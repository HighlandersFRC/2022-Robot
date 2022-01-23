// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.subsystems;

import com.ctre.phoenix.motorcontrol.ControlMode;
import com.ctre.phoenix.motorcontrol.InvertType;
import com.ctre.phoenix.motorcontrol.can.TalonFX;

import edu.wpi.first.wpilibj2.command.SubsystemBase;
import frc.robot.commands.defaults.FeederDefault;

public class Feeder extends SubsystemBase {
  /** Creates a new Feeder. */

    private final TalonFX beltFalcon = new TalonFX(13);
    private final TalonFX lowerFalcon = new TalonFX(14);
    private final TalonFX upperFalcon = new TalonFX(15);

    public Feeder() {}

    public void init() {
        upperFalcon.setInverted(InvertType.InvertMotorOutput);
        setDefaultCommand(new FeederDefault(this));
    }

    public void setBeltFalcon(double percent) {
        beltFalcon.set(ControlMode.PercentOutput, percent);
    }

    public void setLowerFalcon(double percent) {
        lowerFalcon.set(ControlMode.PercentOutput, -percent);
    }

    public void setUpperFalcon(double percent) {
        upperFalcon.set(ControlMode.PercentOutput, percent);
    }

    @Override
    public void periodic() {
        // This method will be called once per scheduler run
    }

    @Override
    public void simulationPeriodic() {
        // This method will be called once per scheduler run during simulation
    }
}
