use std::sync::Mutex;
use tauri::{Manager, RunEvent};
use tauri_plugin_shell::process::CommandChild;
use tauri_plugin_shell::ShellExt;

/// 持有 Python 后端子进程句柄，退出时杀掉
struct BackendProcess(Mutex<Option<CommandChild>>);

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_shell::init())
        .manage(BackendProcess(Mutex::new(None)))
        .setup(|app| {
            // 仅在正式打包后启动内置后端；dev 模式下用户自己跑 python，
            // 避免端口冲突（8000 已被占用时 sidecar 会启动失败）。
            #[cfg(not(debug_assertions))]
            {
                let app_handle = app.handle().clone();
                let sidecar = app_handle
                    .shell()
                    .sidecar("yue-backend")
                    .expect("未找到 sidecar 可执行文件 yue-backend");

                match sidecar.spawn() {
                    Ok((mut rx, child)) => {
                        // 保存子进程句柄，供退出时 kill
                        let state = app.state::<BackendProcess>();
                        *state.0.lock().unwrap() = Some(child);

                        // 后台读日志，避免管道阻塞
                        tauri::async_runtime::spawn(async move {
                            while let Some(event) = rx.recv().await {
                                if let tauri_plugin_shell::process::CommandEvent::Stderr(line) = event {
                                    let msg = String::from_utf8_lossy(&line);
                                    println!("[backend] {}", msg.trim());
                                }
                            }
                        });
                    }
                    Err(e) => {
                        eprintln!("启动内置后端失败: {e}");
                    }
                }
            }
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("error while building tauri application")
        .run(|app_handle, event| {
            // 应用退出时杀掉 Python 子进程，避免残留
            if let RunEvent::ExitRequested { .. } | RunEvent::Exit = event {
                if let Some(state) = app_handle.try_state::<BackendProcess>() {
                    if let Some(child) = state.0.lock().unwrap().take() {
                        let _ = child.kill();
                    }
                }
            }
        });
}
