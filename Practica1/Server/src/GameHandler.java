import java.io.IOException;
import java.net.Socket;

public class GameHandler implements Runnable {
    private Socket sucked;
    private GameProtocol protocol;
    private int estat;
    /*
    TO DO
    Protocol dynamics from Server.
    Methods: run(), init(), play().
     */

    public GameHandler(Socket socket)throws IOException{
        this.sucked = socket;
        this.protocol = new GameProtocol(this.sucked);
        this.estat = 1;
    }



    @Override
    public void run(){
        try {
            while(true){
                play();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void play() throws IOException{
        switch(estat){
            case 1:
                estat = protocol.receiveHelloAndSendReady();
                break;
            case 2:
                estat = protocol.receivePlayAndSendAdmit();
                break;
            case 3:
                estat = protocol.reciveActionAndSendResult();
                break;
            case 4:
                estat = protocol.receivePlayAndSendAdmit();
                break;
        }
    }



}
