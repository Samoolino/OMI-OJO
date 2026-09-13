"use client";

import { useEffect, useRef } from "react";

export default function WebGLGlobe() {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const gl = canvas.getContext("webgl", { antialias: true, alpha: true });
    if (!gl) return;
    const vs = `attribute vec2 p; void main(){gl_Position=vec4(p,0.,1.);}`;
    const fs = `precision mediump float; uniform float t; void main(){vec2 uv=gl_FragCoord.xy/vec2(${canvas.width || 800}.0,${canvas.height || 500}.0); vec2 c=uv-.5; float d=length(c); float glow=smoothstep(.55,.08,d); float rings=sin((d*34.0-t*1.4))*0.5+0.5; vec3 base=vec3(.02,.16,.13); vec3 aqua=vec3(.18,.85,.65); vec3 rain=vec3(.65,1.,.88); float latitude=sin((uv.y-.5)*24.0+t*.2)*.5+.5; vec3 col=mix(base,aqua,glow*.55); col+=rain*pow(max(0.,rings)*glow,5.)*.16; col+=vec3(.02,.25,.18)*latitude*glow*.35; gl_FragColor=vec4(col,glow*.92);}`;
    const compile=(type:number,source:string)=>{const s=gl.createShader(type)!;gl.shaderSource(s,source);gl.compileShader(s);return s};
    const program=gl.createProgram()!;gl.attachShader(program,compile(gl.VERTEX_SHADER,vs));gl.attachShader(program,compile(gl.FRAGMENT_SHADER,fs));gl.linkProgram(program);gl.useProgram(program);
    const buffer=gl.createBuffer()!;gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);
    const loc=gl.getAttribLocation(program,"p");gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);const time=gl.getUniformLocation(program,"t");let frame=0;const start=performance.now();
    const resize=()=>{const r=canvas.getBoundingClientRect();const d=Math.min(devicePixelRatio,2);canvas.width=Math.max(1,r.width*d);canvas.height=Math.max(1,r.height*d);gl.viewport(0,0,canvas.width,canvas.height)};
    resize();window.addEventListener("resize",resize);
    const draw=()=>{gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT);gl.uniform1f(time,(performance.now()-start)/1000);gl.drawArrays(gl.TRIANGLES,0,6);frame=requestAnimationFrame(draw)};draw();
    return()=>{cancelAnimationFrame(frame);window.removeEventListener("resize",resize)};
  },[]);

  return <canvas ref={ref} aria-label="Interactive WebGL climate intelligence globe" />;
}
