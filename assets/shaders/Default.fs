#version 420 core

out vec4 FragColor;

uniform float time; ///< Used to change the color of our stuffs.

void main(){
  //FragColor = mod(vec4(0.3f,0.7f,1.0f,0.0f) * time, 1.0f);
  FragColor = vec4(0.3f,0.7f,1.0f,0.0f);

}
