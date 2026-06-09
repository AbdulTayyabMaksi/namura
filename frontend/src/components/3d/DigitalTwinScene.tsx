"use client";

import { Canvas, useFrame } from "@react-three/fiber";
import { Float, MeshDistortMaterial, OrbitControls, Sphere, Stars } from "@react-three/drei";
import { useRef } from "react";
import * as THREE from "three";

function TwinCore({ color = "#10b981" }: { color?: string }) {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.x = state.clock.elapsedTime * 0.15;
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.2;
    }
  });

  return (
    <Float speed={2} rotationIntensity={0.4} floatIntensity={1.2}>
      <Sphere ref={meshRef} args={[1.2, 64, 64]}>
        <MeshDistortMaterial
          color={color}
          attach="material"
          distort={0.35}
          speed={2}
          roughness={0.2}
          metalness={0.8}
        />
      </Sphere>
    </Float>
  );
}

function OrbitRing({ radius, color, speed }: { radius: number; color: string; speed: number }) {
  const ref = useRef<THREE.Mesh>(null);
  useFrame((state) => {
    if (ref.current) ref.current.rotation.z = state.clock.elapsedTime * speed;
  });
  return (
    <mesh ref={ref} rotation={[Math.PI / 2.5, 0, 0]}>
      <torusGeometry args={[radius, 0.02, 16, 100]} />
      <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.5} />
    </mesh>
  );
}

function DataNodes() {
  const group = useRef<THREE.Group>(null);
  const positions: [number, number, number][] = [
    [2, 0.5, 0], [-2, -0.3, 0.5], [0, 1.5, -1], [1.5, -1, 0.8], [-1, 1, -0.5], [0.5, -1.5, 0.3],
  ];
  const colors = ["#10b981", "#3b82f6", "#8b5cf6", "#f59e0b", "#ef4444", "#06b6d4"];

  useFrame((state) => {
    if (group.current) group.current.rotation.y = state.clock.elapsedTime * 0.08;
  });

  return (
    <group ref={group}>
      {positions.map((pos, i) => (
        <Float key={i} speed={1.5 + i * 0.2} floatIntensity={0.5}>
          <mesh position={pos}>
            <icosahedronGeometry args={[0.15, 1]} />
            <meshStandardMaterial
              color={colors[i]}
              emissive={colors[i]}
              emissiveIntensity={0.6}
              metalness={0.9}
              roughness={0.1}
            />
          </mesh>
        </Float>
      ))}
    </group>
  );
}

interface DigitalTwinSceneProps {
  className?: string;
  interactive?: boolean;
  accentColor?: string;
}

export default function DigitalTwinScene({
  className = "h-full w-full",
  interactive = true,
  accentColor = "#10b981",
}: DigitalTwinSceneProps) {
  return (
    <div className={className} aria-hidden="true">
      <Canvas camera={{ position: [0, 0, 5], fov: 50 }} dpr={[1, 2]}>
        <color attach="background" args={["#0a0f1c"]} />
        <ambientLight intensity={0.3} />
        <pointLight position={[10, 10, 10]} intensity={1.2} color="#10b981" />
        <pointLight position={[-10, -5, -5]} intensity={0.6} color="#8b5cf6" />
        <Stars radius={80} depth={50} count={3000} factor={3} fade speed={0.5} />
        <TwinCore color={accentColor} />
        <OrbitRing radius={1.8} color="#3b82f6" speed={0.3} />
        <OrbitRing radius={2.2} color="#8b5cf6" speed={-0.2} />
        <DataNodes />
        {interactive && (
          <OrbitControls
            enableZoom={false}
            enablePan={false}
            autoRotate
            autoRotateSpeed={0.5}
            maxPolarAngle={Math.PI / 1.8}
            minPolarAngle={Math.PI / 3}
          />
        )}
      </Canvas>
    </div>
  );
}
