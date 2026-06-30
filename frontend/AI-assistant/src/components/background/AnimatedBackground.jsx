import "./background.css";
import DarkVeil from "./DarkVeil";

export default function AnimatedBackground() {
  return (
    <div className="background">
      <DarkVeil
        hueShift={0}
        noiseIntensity={0.01}
        scanlineIntensity={0}
        speed={0.18}
        scanlineFrequency={0}
        warpAmount={0.02}
      />
    </div>
  );
}