#version 420 core

in vec4 frag_color;
out vec4 FragColor;
in vec4 frag_pos;

uniform bool pulse;
uniform float time;

void main(){
  if(pulse){
    vec4 c1 = vec4(1.0,0.0,1.0,0.0);
    vec4 c2 = vec4(0.0,1.0,0.0,1.0);

    float r = mod(time, 1);
    FragColor = mix(c1,c2,r);
    FragColor = mix(FragColor, frag_color, r);
  }
  else{
    FragColor = frag_color;
  }
}
