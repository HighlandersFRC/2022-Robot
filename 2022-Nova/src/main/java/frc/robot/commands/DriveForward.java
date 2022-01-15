// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.commands;

import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj2.command.CommandBase;
import frc.robot.subsystems.Drive;
import frc.robot.tools.math.Vector;

public class DriveForward extends CommandBase {
  /** Creates a new DriveForward. */

  private Drive drive;
  private double distance;
  private boolean isForward;

  private double initTime = 0;

  public DriveForward(Drive drive, double distance, boolean forwardBack) {
    this.drive = drive;
    this.distance = distance;
    this.isForward = forwardBack;
    addRequirements(this.drive);
    // Use addRequirements() here to declare subsystem dependencies.
  }

  // Called when the command is initially scheduled.
  @Override
  public void initialize() {
    initTime = Timer.getFPGATimestamp();
  }

  // Called every time the scheduler runs while the command is scheduled.
  @Override
  public void execute() {
    if(isForward) {
      drive.autoDrive(new Vector(1, 0), 1.5);
    }
    else {
      drive.autoDrive(new Vector(-1, 0), -1.5);
    }
  }

  // Called once the command ends or is interrupted.
  @Override
  public void end(boolean interrupted) {
    // drive.autoDrive, turn, navxOffset);
  }

  // Returns true when the command should end.
  @Override
  public boolean isFinished() {
    if(Timer.getFPGATimestamp() - initTime > 1) {
      return true;
    }
    return false;
  }
}
