package frc.robot.tools;

import edu.wpi.first.wpilibj.DoubleSolenoid;
import edu.wpi.first.wpilibj.PneumaticHub;
import edu.wpi.first.wpilibj.PneumaticsModuleType;
import edu.wpi.first.wpilibj.DoubleSolenoid.Value;

public class PneumaticsControl {
    
    private final PneumaticHub hub = new PneumaticHub();

    private final DoubleSolenoid intakeSolenoid = new DoubleSolenoid(PneumaticsModuleType.REVPH, 8, 9);
    private final DoubleSolenoid leftClimberBrake = new DoubleSolenoid(PneumaticsModuleType.REVPH, 10, 11);
    // private final DoubleSolenoid rightClimberBrake = new DoubleSolenoid(PneumaticsModuleType.REVPH, 10, 11);

    public void setIntakeUp() {
        intakeSolenoid.set(Value.kReverse);
    }

    public void setIntakeDown() {
        intakeSolenoid.set(Value.kForward);
    }

    public void engageClimberBrake() {
        leftClimberBrake.set(Value.kReverse);
    }

    public void releaseClimberBrake() {
        leftClimberBrake.set(Value.kForward);
    }

}
