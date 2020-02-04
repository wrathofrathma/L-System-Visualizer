#version 300 es

precision highp float;
in highp vec4 frag_color;
out highp vec4 FragColor;

uniform float time;

void main(){
  FragColor = frag_color;
}
