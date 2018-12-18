import ApplicationFabric from './ApplicationFabric';
import registerServiceWorker from "react-scripts/template/src/registerServiceWorker";


const fabric = new ApplicationFabric();
const app = fabric.createApplication();
app.run();

registerServiceWorker();