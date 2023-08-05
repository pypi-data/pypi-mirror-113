Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var locale_1 = require("app/locale");
var monitorHeaderActions_1 = tslib_1.__importDefault(require("./monitorHeaderActions"));
var monitorIcon_1 = tslib_1.__importDefault(require("./monitorIcon"));
var MonitorHeader = function (_a) {
    var monitor = _a.monitor, orgId = _a.orgId, onUpdate = _a.onUpdate;
    return (<div className="release-details">
    <div className="row">
      <div className="col-sm-6 col-xs-10">
        <h3>{monitor.name}</h3>
        <div className="release-meta">{monitor.id}</div>
      </div>
      <div className="col-sm-2 hidden-xs">
        <h6 className="nav-header">{locale_1.t('Last Check-in')}</h6>
        {monitor.lastCheckIn && <timeSince_1.default date={monitor.lastCheckIn}/>}
      </div>
      <div className="col-sm-2 hidden-xs">
        <h6 className="nav-header">{locale_1.t('Next Check-in')}</h6>
        {monitor.nextCheckIn && <timeSince_1.default date={monitor.nextCheckIn}/>}
      </div>
      <div className="col-sm-2">
        <h6 className="nav-header">{locale_1.t('Status')}</h6>
        <monitorIcon_1.default status={monitor.status} size={16}/>
      </div>
    </div>
    <monitorHeaderActions_1.default orgId={orgId} monitor={monitor} onUpdate={onUpdate}/>
  </div>);
};
exports.default = MonitorHeader;
//# sourceMappingURL=monitorHeader.jsx.map