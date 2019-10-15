#version 420 core

in vec4 frag_color;
out vec4 FragColor;

uniform float time;

void main(){
  FragColor = frag_color;
}
