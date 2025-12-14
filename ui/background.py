import pyglet
from config.consts import PALETTES, settings # Import settings

vertex_source = """
#version 330
in vec2 position;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment_source = """
#version 330
out vec4 final_color;

uniform float u_time;
uniform vec2 u_resolution;
uniform vec3 u_color1;
uniform vec3 u_color2;
uniform vec3 u_color3;

// Nowy uniform sterowany suwakiem
uniform float u_pixels;

void main() {
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;

    // Używamy uniforma zamiast stałej liczby
    // max(10.0, ...) zabezpiecza przed dzieleniem przez 0
    float p = max(10.0, u_pixels);

    uv = floor(uv * p) / p;

    float t = u_time * 0.5;
    float v = 0.0;
    vec2 c = uv * 2.5 - vec2(2.0);

    v += sin(c.x + t);
    v += sin((c.y + t) / 2.0);
    v += sin((c.x + c.y + t) / 2.0);
    c += vec2(sin(t / 3.0), cos(t / 2.0));
    v += sin(sqrt(c.x * c.x + c.y * c.y + 1.0) + t);

    vec3 color = mix(u_color1, u_color2, sin(v * 3.0) * 0.5 + 0.5);
    color = mix(color, u_color3, sin(v * 5.0 + t) * 0.2);

    final_color = vec4(color, 1.0);
}
"""

class ShaderBackground:
    def __init__(self, width, height):
        try:
            self.program = pyglet.graphics.shader.ShaderProgram(
                pyglet.graphics.shader.Shader(vertex_source, 'vertex'),
                pyglet.graphics.shader.Shader(fragment_source, 'fragment')
            )
        except pyglet.gl.GLException as e:
            print(f"Błąd shadera: {e}")
            raise

        self.time = 0.0
        self.vlist = self.program.vertex_list(4, pyglet.gl.GL_TRIANGLE_STRIP, batch=None,
            position=('f', (-1, -1,  1, -1,  -1, 1,  1, 1))
        )

        # Kolory
        self.current_palette_idx = 0
        self.palette_timer = 0.0
        self.switch_time = 15.0
        p = PALETTES[0]
        self.curr_c1, self.target_c1 = list(p["c1"]), list(p["c1"])
        self.curr_c2, self.target_c2 = list(p["c2"]), list(p["c2"])
        self.curr_c3, self.target_c3 = list(p["c3"]), list(p["c3"])

    def lerp_color(self, current, target, dt, speed=1.0):
        return [c + (t - c) * dt * speed for c, t in zip(current, target)]

    def update(self, dt, width, height):
        self.time += dt
        self.palette_timer += dt

        if self.palette_timer > self.switch_time:
            self.palette_timer = 0
            self.current_palette_idx = (self.current_palette_idx + 1) % len(PALETTES)
            new_p = PALETTES[self.current_palette_idx]
            self.target_c1 = list(new_p["c1"])
            self.target_c2 = list(new_p["c2"])
            self.target_c3 = list(new_p["c3"])

        speed = 0.8
        self.curr_c1 = self.lerp_color(self.curr_c1, self.target_c1, dt, speed)
        self.curr_c2 = self.lerp_color(self.curr_c2, self.target_c2, dt, speed)
        self.curr_c3 = self.lerp_color(self.curr_c3, self.target_c3, dt, speed)

        self.program['u_time'] = self.time
        self.program['u_resolution'] = (float(width), float(height))
        self.program['u_color1'] = tuple(self.curr_c1)
        self.program['u_color2'] = tuple(self.curr_c2)
        self.program['u_color3'] = tuple(self.curr_c3)

        # PRZEKAZUJEMY WARTOŚĆ Z USTAWIEŃ DO SHADERA
        # settings.crt_intensity steruje "wielkością pikseli" w shaderze
        self.program['u_pixels'] = float(settings.crt_intensity)

    def draw(self):
        self.program.use()
        self.vlist.draw(pyglet.gl.GL_TRIANGLE_STRIP)
        self.program.stop()