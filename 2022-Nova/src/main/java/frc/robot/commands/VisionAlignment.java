// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.commands;

import edu.wpi.first.wpilibj2.command.CommandBase;
import frc.robot.Constants;
import frc.robot.subsystems.Drive;
import frc.robot.subsystems.MqttPublish;
import frc.robot.subsystems.MqttSubscribe;
import frc.robot.subsystems.Peripherals;
import frc.robot.tools.controlloops.PID;
import frc.robot.tools.math.Vector;

public class VisionAlignment extends CommandBase {
  /** Creates a new VisionAlignment. */

  private Peripherals peripherals;
  private Drive drive;
  private MqttSubscribe subscribe;

  private PID pid= new PID(0.1, 0, 0);

  private double currentCameraAngle = 0;
  // private boolean check;

  public VisionAlignment(Drive drive, Peripherals peripherals, MqttSubscribe subscribe) {
    this.peripherals = peripherals;
    this.drive = drive;
    this.subscribe = subscribe;
    addRequirements(peripherals, drive);
    // Use addRequirements() here to declare subsystem dependencies.
  }

  // Called when the command is initially scheduled.
  @Override
  public void initialize() {
    peripherals.turnLightRingOn();
    currentCameraAngle = subscribe.getLastMessageVal();
    pid.setSetPoint(0);
    pid.setMaxOutput(-1);
    pid.setMinOutput(-1);
  }

  // Called every time the scheduler runs while the command is scheduled.
  @Override
  public void execute() {
    currentCameraAngle = subscribe.getLastMessageVal();

    pid.updatePID(currentCameraAngle);
    System.out.println(pid.getResult());
    drive.autoDrive(new Vector(0, 0), pid.getResult() * (Constants.TOP_SPEED)/(Constants.ROBOT_RADIUS));
  }

  // Called once the command ends or is interrupted.
  @Override
  public void end(boolean interrupted) {
    peripherals.turnLightRingOff();
  }

  // Returns true when the command should end.
  @Override
  public boolean isFinished() {
    return false;
  }
}
