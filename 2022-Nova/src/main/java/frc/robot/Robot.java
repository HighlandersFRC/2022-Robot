package frc.robot;

import edu.wpi.first.wpilibj.TimedRobot;
import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.CommandScheduler;
import frc.robot.commands.ContinuousAccelerationInterpolation;
import frc.robot.commands.DriveForward;
import frc.robot.commands.EjectBalls;
import frc.robot.commands.FireBalls;
import frc.robot.commands.IntakeBalls;
import frc.robot.commands.IntakeUp;
import frc.robot.commands.SetHoodPosition;
import frc.robot.commands.SpinShooter;
import frc.robot.commands.VisionAlignment;
import frc.robot.subsystems.Drive;
import frc.robot.subsystems.IntakeFeeder;
import frc.robot.subsystems.LinearActuator;
import frc.robot.subsystems.MqttPublish;
import frc.robot.subsystems.MqttSubscribe;
import frc.robot.subsystems.Peripherals;
import frc.robot.subsystems.Shooter;
import frc.robot.tools.PneumaticsControl;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import org.json.JSONArray;
import org.json.JSONTokener;

public class Robot extends TimedRobot {
  private Command m_autonomousCommand;

  private RobotContainer m_robotContainer;
  File f;
  BufferedWriter bw;
  FileWriter fw;
  double startTime;

  File pathingFile;
  String pathString;

  JSONArray pathJSON;

  ContinuousAccelerationInterpolation testPath;

  private final Peripherals peripherals = new Peripherals();
  private final Drive drive = new Drive(peripherals);
  private final Shooter shooter = new Shooter();
  private final LinearActuator linearActuator = new LinearActuator();

  private final PneumaticsControl pneumatics = new PneumaticsControl();
  
  private final IntakeFeeder intakeFeeder = new IntakeFeeder(pneumatics);

  private final String subCameraTopic = "/sensors/camera";
  private final String pubCameraTopic = "/robot/camera";

  private MqttPublish publish = new MqttPublish();
  private MqttSubscribe subscribe = new MqttSubscribe();


  /**
   * This function is run when the robot is first started up and should be used
   * for any initialization code.
   */
  @Override
  public void robotInit() {
    // System.out.println("###########");
    drive.init();
    peripherals.init();
    intakeFeeder.init();
    shooter.init();
    linearActuator.init();

    // publish.publish(pubCameraTopic);
    subscribe.subscribe(subCameraTopic);
    m_robotContainer = new RobotContainer();

    try {
      pathingFile = new File("/home/lvuser/deploy/RotateTest.json");
      FileReader scanner = new FileReader(pathingFile);
      pathJSON = new JSONArray(new JSONTokener(scanner));
    }
    catch(Exception e) {
      System.out.println("ERROR WITH PATH FILE " + e);
    }
  }

  @Override
  public void robotPeriodic() {
    // SmartDashboard.putNumber("Navx Value", peripherals.getNavxAngle());
    // System.out.println("^^^^^^^^^^^^^^^^^^^ " + drive.getOdometryAngle());
    CommandScheduler.getInstance().run();
    // System.out.println(">>>>>>>>>>>>>>>>>>> " + drive.getOdometryAngle());
    // System.out.println(Math.toDegrees(peripherals.getNavxAngle()));
    intakeFeeder.periodic();
    }
  

  /** This function is called once each time the robot enters Disabled mode. */
  @Override
  public void disabledInit() {
    try {
      if(bw != null){ 
        bw.close();
      }
      if(fw != null){
        fw.close();
      }
     
    } catch (IOException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
    
  }

  @Override
  public void disabledPeriodic() {}

  @Override
  public void autonomousInit() {
    drive.autoInit(pathJSON);
    // peripherals.init();
    testPath = new ContinuousAccelerationInterpolation(drive, pathJSON);
    testPath.schedule();
  }

  /** This function is called periodically during autonomous. */
  @Override
  public void autonomousPeriodic() {}

  @Override
  public void teleopInit() {
    startTime = Timer.getFPGATimestamp();
    intakeFeeder.teleopInit();
    // try{
    //   f = new File("/home/lvuser/Navx/NavxValues" +  (int) startTime + ".csv");
    //   if(!f.exists()){
    //     f.createNewFile();  
    //   }
    //   fw = new FileWriter(f);
    //   bw = new BufferedWriter(fw);
    //   bw.write("started collecting \n" );
      
      
    //   }
    //   catch (Exception e){
    //     e.printStackTrace();
    //   }

    if (m_autonomousCommand != null) {
      m_autonomousCommand.cancel();
    }

    // OI.driverA.whenPressed(new DriveForward(drive, 2, true));
    // OI.driverB.whenPressed(new DriveForward(drive, 2, false));

    OI.driverRT.whileHeld(new IntakeBalls(intakeFeeder));
    OI.driverLT.whileHeld(new EjectBalls(intakeFeeder, 0.4));
    // OI.driverB.whileHeld(new IntakeUp(intake));

    OI.driverA.whileHeld(new SetHoodPosition(linearActuator, 0.2));
    OI.driverB.whileHeld(new SetHoodPosition(linearActuator, 0.4));
    OI.driverY.whileHeld(new SetHoodPosition(linearActuator, 0.95));

    OI.driverX.whenPressed(new FireBalls(intakeFeeder, shooter, linearActuator));

    // OI.driverB.whileHeld(new SpinShooter(shooter, 0.5));

    OI.driverX.whenReleased(new SetHoodPosition(linearActuator, 0));
    OI.driverX.whenReleased(new EjectBalls(intakeFeeder, 0));
    OI.driverX.whenReleased(new SpinShooter(shooter, 0));


  }

  /** This function is called periodically during operator control. */
  @Override
  public void teleopPeriodic() {
    // System.out.println(pathJSON.toString());
    //    try{
    //   bw.write(Timer.getFPGATimestamp() - startTime + ",");
    //   bw.write( peripherals.getNavxYaw() + ",");
    //   bw.write( peripherals.getNavxRoll() + ",");
    //   bw.write( peripherals.getNavxPitch() + "\n");
    // } catch (Exception e){
    //   e.printStackTrace();
    // }
    SmartDashboard.putNumber("Controller Y", OI.getDriverLeftY());
    SmartDashboard.putNumber("Controller X", OI.getDriverLeftX());
  }

  @Override
  public void testInit() {
    OI.driverRT.whileHeld(new IntakeBalls(intakeFeeder));
    // Cancels all running commands at the start of test mode.
    CommandScheduler.getInstance().cancelAll();
  }

  /** This function is called periodically during test mode. */
  @Override
  public void testPeriodic() {}
}
