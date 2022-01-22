package frc.robot.tools;

import edu.wpi.first.wpilibj.DoubleSolenoid;
import edu.wpi.first.wpilibj.PneumaticHub;
import edu.wpi.first.wpilibj.PneumaticsModuleType;
import edu.wpi.first.wpilibj.DoubleSolenoid.Value;

public class PneumaticsControl {
    
    private final PneumaticHub hub = new PneumaticHub();

    private final DoubleSolenoid intakeSolenoid = new DoubleSolenoid(PneumaticsModuleType.REVPH, 6, 7);

    public void setIntakeUp() {
        intakeSolenoid.set(Value.kForward);
    }

    public void setIntakeDown() {
        intakeSolenoid.set(Value.kReverse);
    }

}
