Object.defineProperty(exports, "__esModule", { value: true });
exports.SingleAxisChart = void 0;
var tslib_1 = require("tslib");
var durationChart_1 = tslib_1.__importDefault(require("../chart/durationChart"));
var histogramChart_1 = tslib_1.__importDefault(require("../chart/histogramChart"));
var utils_1 = require("./utils");
function SingleAxisChart(props) {
    var axis = props.axis, onFilterChange = props.onFilterChange, eventView = props.eventView, organization = props.organization, location = props.location, didReceiveMultiAxis = props.didReceiveMultiAxis, usingBackupAxis = props.usingBackupAxis;
    var backupField = utils_1.getBackupField(axis);
    function didReceiveMulti(dataCounts) {
        if (!didReceiveMultiAxis) {
            return;
        }
        if (dataCounts[axis.field]) {
            didReceiveMultiAxis(false);
            return;
        }
        if (backupField && dataCounts[backupField]) {
            didReceiveMultiAxis(true);
            return;
        }
    }
    var axisOrBackup = utils_1.getAxisOrBackupAxis(axis, usingBackupAxis);
    return axis.isDistribution ? (<histogramChart_1.default field={axis.field} eventView={eventView} organization={organization} location={location} onFilterChange={onFilterChange} title={axisOrBackup.label} titleTooltip={axisOrBackup.tooltip} didReceiveMultiAxis={didReceiveMulti} usingBackupAxis={usingBackupAxis} backupField={backupField}/>) : (<durationChart_1.default field={axis.field} eventView={eventView} organization={organization} title={axisOrBackup.label} titleTooltip={axisOrBackup.tooltip} usingBackupAxis={usingBackupAxis} backupField={backupField}/>);
}
exports.SingleAxisChart = SingleAxisChart;
//# sourceMappingURL=singleAxisChart.jsx.map