// Pip 桌面寵物：全螢幕透明置頂視窗
// - 預設滑鼠穿透；前端判斷游標在 Pip 身上時呼叫 set_through(false) 讓牠可以被點
// - 穿透時網頁收不到 mousemove，所以由 Rust 每 30ms 讀游標位置推給前端（Tauri 沒有 Electron 的 forward:true）
// - 127.0.0.1:38917/state?mode=exec&tool=Bash 接收 Claude 狀態（之後由 Mod 打過來）
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::collections::HashMap;
use std::thread;
use std::time::Duration;

use tauri::menu::{Menu, MenuItem};
use tauri::tray::TrayIconBuilder;
use tauri::{Emitter, Manager, PhysicalPosition, PhysicalSize, WebviewWindow};

const STATE_ADDR: &str = "127.0.0.1:38917";

#[tauri::command]
fn set_through(window: WebviewWindow, through: bool) {
    let _ = window.set_ignore_cursor_events(through);
}

#[derive(Clone, serde::Serialize)]
struct Cursor {
    x: f64,
    y: f64,
}

fn parse_query(url: &str) -> HashMap<String, String> {
    url.split_once('?')
        .map(|(_, q)| q)
        .unwrap_or("")
        .split('&')
        .filter_map(|kv| kv.split_once('='))
        .map(|(k, v)| (k.to_string(), v.replace("%20", " ")))
        .collect()
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![set_through])
        .setup(|app| {
            let win = app.get_webview_window("main").expect("main window");

            // 鋪滿主螢幕的工作區（不蓋工作列），Pip 站在工作列上緣
            if let Some(mon) = app.primary_monitor()? {
                let area = mon.work_area();
                win.set_position(PhysicalPosition::new(area.position.x, area.position.y))?;
                win.set_size(PhysicalSize::new(area.size.width, area.size.height))?;
            }
            win.set_ignore_cursor_events(true)?;
            win.show()?;

            // 系統匣：顯示／隱藏、結束
            let toggle = MenuItem::with_id(app, "toggle", "隱藏 Pip", true, None::<&str>)?;
            let quit = MenuItem::with_id(app, "quit", "結束 Pip", true, None::<&str>)?;
            let menu = Menu::with_items(app, &[&toggle, &quit])?;
            let toggle2 = toggle.clone();
            TrayIconBuilder::with_id("pip")
                .icon(app.default_window_icon().cloned().expect("icon"))
                .tooltip("Pip")
                .menu(&menu)
                .on_menu_event(move |app, ev| match ev.id().as_ref() {
                    "toggle" => {
                        if let Some(w) = app.get_webview_window("main") {
                            if w.is_visible().unwrap_or(true) {
                                let _ = w.hide();
                                let _ = toggle2.set_text("顯示 Pip");
                            } else {
                                let _ = w.show();
                                let _ = w.set_ignore_cursor_events(true);
                                let _ = toggle2.set_text("隱藏 Pip");
                            }
                        }
                    }
                    "quit" => app.exit(0),
                    _ => {}
                })
                .build(app)?;

            // 游標輪詢 → 轉成視窗內的 CSS 像素
            let handle = app.handle().clone();
            let w2 = win.clone();
            thread::spawn(move || loop {
                if let (Ok(c), Ok(p), Ok(s)) =
                    (handle.cursor_position(), w2.outer_position(), w2.scale_factor())
                {
                    let _ = handle.emit(
                        "cursor",
                        Cursor { x: (c.x - p.x as f64) / s, y: (c.y - p.y as f64) / s },
                    );
                }
                thread::sleep(Duration::from_millis(30));
            });

            // 狀態端點
            let handle = app.handle().clone();
            thread::spawn(move || {
                let server = match tiny_http::Server::http(STATE_ADDR) {
                    Ok(s) => s,
                    Err(e) => {
                        eprintln!("state server failed on {STATE_ADDR}: {e}");
                        return;
                    }
                };
                for req in server.incoming_requests() {
                    let q = parse_query(req.url());
                    if !q.is_empty() {
                        let _ = handle.emit("state", q);
                    }
                    let _ = req.respond(tiny_http::Response::from_string("ok"));
                }
            });
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running Pip");
}
