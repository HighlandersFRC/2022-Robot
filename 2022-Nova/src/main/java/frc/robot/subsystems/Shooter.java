// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.subsystems;

import com.ctre.phoenix.motorcontrol.ControlMode;
import com.ctre.phoenix.motorcontrol.can.TalonFX;

import edu.wpi.first.wpilibj2.command.SubsystemBase;
import frc.robot.commands.defaults.IntakeDefault;
import frc.robot.commands.defaults.ShooterDefault;
import frc.robot.tools.PneumaticsControl;

public class Shooter extends SubsystemBase {

  private final TalonFX shooterMaster = new TalonFX(10);
  private final TalonFX shooterFollower = new TalonFX(9);

  /** Creates a new Intake. */
  public Shooter() {
    
  }

  public void init() {
    shooterFollower.set(ControlMode.Follower, 10);
    setDefaultCommand(new ShooterDefault(this));
  }

  public void setShooterPercent(double percent) {
    shooterMaster.set(ControlMode.PercentOutput, percent);
  }

  @Override
  public void periodic() {
    // This method will be called once per scheduler run
  }
}
