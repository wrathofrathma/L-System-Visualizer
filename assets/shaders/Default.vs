#version 420 core

layout(location = 0) in vec2 vpos;

void main(){
  gl_Position = vec4(vpos,0.0,0.0);
}
