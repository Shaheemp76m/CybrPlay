import raylib

raylib.InitWindow(800, 500, b"test")

while not raylib.WindowShouldClose():
        raylib.BeginDrawing()
        raylib.ClearBackground(raylib.BLACK)
        raylib.EndDrawing()

raylib.CloseWindow()
