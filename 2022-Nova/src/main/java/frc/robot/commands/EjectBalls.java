// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.commands;

import edu.wpi.first.wpilibj2.command.CommandBase;
import frc.robot.subsystems.IntakeFeeder;

public class EjectBalls extends CommandBase {
  /** Creates a new EjectBalls. */

  private IntakeFeeder intakeFeeder;
  private double feederPercent;

  public EjectBalls(IntakeFeeder intakeFeeder, double percent) {
    this.intakeFeeder = intakeFeeder;
    this.feederPercent = percent;
    addRequirements(intakeFeeder);
    // Use addRequirements() here to declare subsystem dependencies.
  }

  // Called when the command is initially scheduled.
  @Override
  public void initialize() {}

  // Called every time the scheduler runs while the command is scheduled.
  @Override
  public void execute() {
    intakeFeeder.setUpperFalcon(feederPercent);
    intakeFeeder.setLowerFalcon(feederPercent);
    intakeFeeder.setBeltFalcon(feederPercent);
  }

  // Called once the command ends or is interrupted.
  @Override
  public void end(boolean interrupted) {
    intakeFeeder.setBallCount(0);
  }

  // Returns true when the command should end.
  @Override
  public boolean isFinished() {
    return false;
  }
}
