import os, subprocess, re, time, math, random, threading
import pygame

# ----------------------------
# 0️⃣ macOS Safe Init
# ----------------------------
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# ----------------------------
# 1️⃣ Lid angle (threaded poller)
# ----------------------------
current_angle = 0.0
lock = threading.Lock()

def poll_lid_angle():
    global current_angle
    script = '''
    tell application "System Events"
        tell application process "LidAngleSensor"
            try
                set v to value of static text 1 of window 1
                return v
            on error
                return ""
            end try
        end tell
    end tell
    '''
    while True:
        try:
            out = subprocess.check_output(["osascript", "-e", script],
                                          stderr=subprocess.DEVNULL).decode().strip()
            match = re.search(r"(\d+(\.\d+)?)", out)
            val = float(match.group(1)) if match else current_angle
            with lock:
                current_angle = val
        except Exception:
            pass
        time.sleep(0.5)  # 🔥 ~2 reads per second

threading.Thread(target=poll_lid_angle, daemon=True).start()

def get_lid_angle():
    with lock:
        return current_angle


# ----------------------------
# 2️⃣ Setup + Sounds
# ----------------------------
pygame.init()
pygame.mixer.init(frequency=44100, channels=16, buffer=256)
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("🎛️ MacHarmonium — Fast Mode")

FONT_BIG = pygame.font.SysFont("Menlo", 28, bold=True)
FONT_SMALL = pygame.font.SysFont("Menlo", 18)

note_map = {
    pygame.K_a: "c4.wav", pygame.K_s: "d4.wav", pygame.K_d: "e4.wav",
    pygame.K_f: "f4.wav", pygame.K_g: "g4.wav", pygame.K_h: "a4.wav",
    pygame.K_j: "b4.wav", pygame.K_k: "c5.wav"
}
note_sounds = {k: pygame.mixer.Sound(v) for k, v in note_map.items()}

active_channels = {}
drone_channel = None
air_pressure = 0.0
target_pressure = 0.0
last_angle = 0
last_time = time.time()
mode_index = 0
modes = ["Bellows", "Pitch Bend", "Filter", "Chaos"]
running = True

# ----------------------------
# 3️⃣ Physics
# ----------------------------
def update_bellows(angle, dt):
    global air_pressure, target_pressure, last_angle
    velocity = (angle - last_angle) / max(dt, 1e-4)
    target_pressure = max(0.0, min(angle / 135.0, 1.0))
    # faster smoothing for responsiveness
    air_pressure += (target_pressure - air_pressure) * 0.25
    burst = max(0.0, min(abs(velocity) / 250.0, 0.4))
    air_pressure = min(1.0, air_pressure + burst)
    last_angle = angle
    return air_pressure, velocity


# ----------------------------
# 4️⃣ Helpers
# ----------------------------
def play_key(key):
    if key not in active_channels:
        ch = note_sounds[key].play(-1)
        ch.set_volume(0)
        active_channels[key] = ch

def stop_key(key):
    if key in active_channels:
        active_channels[key].fadeout(100)
        del active_channels[key]

def draw_knob(x, y, value, label):
    radius = 50
    end_angle = value * math.pi * 1.5 + math.pi * 0.75
    pygame.draw.circle(screen, (40, 40, 60), (x, y), radius)
    pygame.draw.arc(screen, (0, 255, 255),
                    (x - radius, y - radius, radius*2, radius*2),
                    math.pi * 0.75, end_angle, 8)
    txt = FONT_SMALL.render(label, True, (200, 200, 200))
    screen.blit(txt, (x - 40, y + 60))

def draw_gradient(angle):
    hue = int((angle / 135) * 255)
    color1 = (hue, 100, 255 - hue)
    color2 = (10, 10, 15)
    for y in range(600):
        ratio = y / 600
        r = int(color1[0]*(1-ratio)+color2[0]*ratio)
        g = int(color1[1]*(1-ratio)+color2[1]*ratio)
        b = int(color1[2]*(1-ratio)+color2[2]*ratio)
        pygame.draw.line(screen, (r,g,b), (0,y),(900,y))

def pulse_color(base):
    t = time.time() * 2
    mod = (math.sin(t) + 1) / 2
    return (int(base[0]*mod), int(base[1]*mod), int(base[2]*mod))


# ----------------------------
# 5️⃣ Main Loop
# ----------------------------
clock = pygame.time.Clock()
angle = 0
velocity = 0
print("🎹 Fast Mode: focus the window, play A–K, hinge = volume")

while running:
    start = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                mode_index = (mode_index + 1) % len(modes)
            elif event.key == pygame.K_SPACE:
                if not drone_channel:
                    drone_channel = note_sounds[pygame.K_a].play(-1)
                    drone_channel.set_volume(0)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and drone_channel:
                drone_channel.fadeout(300)
                drone_channel = None

    keys = pygame.key.get_pressed()
    for k in note_map.keys():
        if keys[k]:
            play_key(k)
        else:
            stop_key(k)

    angle_new = get_lid_angle() or angle
    dt = time.time() - start
    air, velocity = update_bellows(angle_new, dt)
    angle = angle_new
    loud = math.pow(air, 1.8)

    for k, ch in active_channels.items():
        ch.set_volume(loud)
    if drone_channel:
        drone_channel.set_volume(loud * 0.6)

    # Draw
    draw_gradient(angle)
    draw_knob(150, 300, angle/135, "Angle")
    draw_knob(350, 300, air, "Pressure")
    draw_knob(550, 300, abs(velocity)/400, "Velocity")

    title = FONT_BIG.render("🎶 MacHarmonium (Fast Mode)", True, pulse_color((255,100,255)))
    mode_txt = FONT_SMALL.render(f"Mode: {modes[mode_index]}", True, (220,255,220))
    held_txt = FONT_SMALL.render(
        f"Keys: {' '.join([pygame.key.name(k) for k in active_channels]) or 'None'}",
        True, (180,220,255)
    )
    screen.blit(title, (230, 40))
    screen.blit(mode_txt, (360, 100))
    screen.blit(held_txt, (340, 130))

    pygame.display.flip()
    clock.tick(120)  # 🚀 high refresh

pygame.quit()
