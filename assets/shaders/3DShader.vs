#version 300 es

layout(location = 0) in vec3 vpos;
layout(location = 1) in vec4 vcolor;

uniform mat4 model; // Model matrix
uniform mat4 view; // View matrix
uniform mat4 proj; // Projection matrix

out vec4 frag_pos; // Our vertex position in model coordinates.
out vec4 frag_color; // Our fragment color

void main(){
  frag_pos = model * vec4(vpos, 1.0);
  gl_Position = proj * view * model * vec4(vpos,1.0);
  frag_color = vcolor;
}
