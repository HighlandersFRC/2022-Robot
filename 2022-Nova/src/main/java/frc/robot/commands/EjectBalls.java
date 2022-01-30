// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.commands;

import edu.wpi.first.wpilibj2.command.CommandBase;
import frc.robot.subsystems.Feeder;

public class EjectBalls extends CommandBase {
  /** Creates a new EjectBalls. */

  private Feeder feeder;
  private double feederPercent;

  public EjectBalls(Feeder feeder, double percent) {
    this.feeder = feeder;
    this.feederPercent = percent;
    addRequirements(feeder);
    // Use addRequirements() here to declare subsystem dependencies.
  }

  // Called when the command is initially scheduled.
  @Override
  public void initialize() {}

  // Called every time the scheduler runs while the command is scheduled.
  @Override
  public void execute() {
    feeder.setUpperFalcon(feederPercent);
    feeder.setLowerFalcon(feederPercent);
    feeder.setBeltFalcon(feederPercent);
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
