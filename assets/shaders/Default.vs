#version 420 core

layout(location = 0) in vec4 vpos;

void main(){
  gl_Position = vpos;
}
