import java.io.IOException;
import java.net.Socket;

public class GameClient{

    private Socket sucked;
    private ClientProtocol protocol;
    private boolean fi;
    private int estat;
    /*
    TO DO.
    Class that encapsulates the game's logic. Sequence of states following the established protocol .
     */

    public GameClient(Socket socket) throws IOException{
        this.sucked = socket;
        this.protocol = new ClientProtocol(this.sucked);
        this.fi = false;
        this.estat = 1;
    }
    public boolean getFinally(){
        return this.fi;
    }

    public void setFi(boolean fi){
        this.fi = fi;
    }
    public void play() throws IOException{
        switch (estat){
            case 1: 
                estat =  protocol.sendHello();
                break;
            case 2:
                estat = protocol.receiveReadyAndSendPlay();
                break;
            case 3: 
                estat = protocol.receiveAdmitAndSendAction();
                break;
            case 4:
                estat = protocol.receiveResultandSendAction();
                break;
            case 5:
                setFi(true);
                break;
        }
    }


}
