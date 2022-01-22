// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.subsystems;

import com.ctre.phoenix.motorcontrol.ControlMode;
import com.ctre.phoenix.motorcontrol.can.TalonFX;

import edu.wpi.first.wpilibj2.command.SubsystemBase;
import frc.robot.commands.defaults.IntakeDefault;
import frc.robot.tools.PneumaticsControl;

public class Intake extends SubsystemBase {

  private PneumaticsControl pneumatics;

  private final TalonFX intakeMotor = new TalonFX(12);

  /** Creates a new Intake. */
  public Intake(PneumaticsControl pneumatics) {
    this.pneumatics = pneumatics;
  }

  public void init() {
    setDefaultCommand(new IntakeDefault(this));
  }

  public void setIntakeUp() {
    pneumatics.setIntakeUp();
  }

  public void setIntakeDown() {
    pneumatics.setIntakeDown();
  }

  public void setIntakePercent(double percent) {
    intakeMotor.set(ControlMode.PercentOutput, percent);
  }

  @Override
  public void periodic() {
    // This method will be called once per scheduler run
  }
}
