// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.commands;

import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj2.command.CommandBase;
import frc.robot.subsystems.IntakeFeeder;

public class IntakeBalls extends CommandBase {
  private static IntakeFeeder intakeFeeder;
  double time = 0;

  public IntakeBalls(IntakeFeeder intakeFeeder) {
    this.intakeFeeder = intakeFeeder;
    addRequirements(this.intakeFeeder);
  }

  // Called when the command is initially scheduled.
  @Override
  public void initialize() {
    time = Timer.getFPGATimestamp();
  }

  // Called every time the scheduler runs while the command is scheduled.
  @Override
  public void execute() {
    intakeFeeder.setIntakeDown();
    intakeFeeder.setIntakePercent(-0.4);

    if (!intakeFeeder.getTopBeamBreak()) {
      if (!intakeFeeder.getBottomBeamBreak()) {
        if (Timer.getFPGATimestamp() - time >= 0.2) {
          intakeFeeder.setLowerFalcon(0);
          intakeFeeder.setBeltFalcon(0);
          intakeFeeder.setBallCount(2);
        }
      } else {
        time = Timer.getFPGATimestamp();
        if (intakeFeeder.getBallCount() < 2) {
          intakeFeeder.setBeltFalcon(0.2);
          intakeFeeder.setLowerFalcon(0.2);
        }
        intakeFeeder.setBeltFalcon(0);
        intakeFeeder.setLowerFalcon(0);
      }
    } else {
      intakeFeeder.setBeltFalcon(0.2);
      intakeFeeder.setLowerFalcon(0.2);
    }
  }

  // Called once the command ends or is interrupted.
  @Override
  public void end(boolean interrupted) {}

  // Returns true when the command should end.
  @Override
  public boolean isFinished() {
    return false;
  }
}
