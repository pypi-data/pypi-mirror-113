Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var forms_1 = require("app/components/forms");
var internalStatChart_1 = tslib_1.__importDefault(require("app/components/internalStatChart"));
var panels_1 = require("app/components/panels");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var TIME_WINDOWS = ['1h', '1d', '1w'];
var AdminQueue = /** @class */ (function (_super) {
    tslib_1.__extends(AdminQueue, _super);
    function AdminQueue() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AdminQueue.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { timeWindow: '1w', since: new Date().getTime() / 1000 - 3600 * 24 * 7, resolution: '1h', taskName: null });
    };
    AdminQueue.prototype.getEndpoints = function () {
        return [['taskList', '/internal/queue/tasks/']];
    };
    AdminQueue.prototype.changeWindow = function (timeWindow) {
        var seconds;
        if (timeWindow === '1h') {
            seconds = 3600;
        }
        else if (timeWindow === '1d') {
            seconds = 3600 * 24;
        }
        else if (timeWindow === '1w') {
            seconds = 3600 * 24 * 7;
        }
        else {
            throw new Error('Invalid time window');
        }
        this.setState({
            since: new Date().getTime() / 1000 - seconds,
            timeWindow: timeWindow,
        });
    };
    AdminQueue.prototype.changeTask = function (value) {
        this.setState({ activeTask: value });
    };
    AdminQueue.prototype.renderBody = function () {
        var _this = this;
        var _a = this.state, activeTask = _a.activeTask, taskList = _a.taskList;
        return (<div>
        <Header>
          <h3 className="no-border">Queue Overview</h3>

          <buttonBar_1.default merged active={this.state.timeWindow}>
            {TIME_WINDOWS.map(function (r) { return (<button_1.default size="small" barId={r} onClick={function () { return _this.changeWindow(r); }} key={r}>
                {r}
              </button_1.default>); })}
          </buttonBar_1.default>
        </Header>

        <panels_1.Panel>
          <panels_1.PanelHeader>Global Throughput</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <internalStatChart_1.default since={this.state.since} resolution={this.state.resolution} stat="jobs.all.started" label="jobs started"/>
          </panels_1.PanelBody>
        </panels_1.Panel>

        <h3 className="no-border">Task Details</h3>

        <div>
          <div className="m-b-1">
            <label>Show details for task:</label>
            <forms_1.SelectField name="task" onChange={function (value) { return _this.changeTask(value); }} value={activeTask} clearable choices={taskList.map(function (t) { return [t, t]; })}/>
          </div>
          {activeTask ? (<div>
              <panels_1.Panel key={"jobs.started." + activeTask}>
                <panels_1.PanelHeader>
                  Jobs Started <small>{activeTask}</small>
                </panels_1.PanelHeader>
                <panels_1.PanelBody withPadding>
                  <internalStatChart_1.default since={this.state.since} resolution={this.state.resolution} stat={"jobs.started." + activeTask} label="jobs" height={100}/>
                </panels_1.PanelBody>
              </panels_1.Panel>
              <panels_1.Panel key={"jobs.finished." + activeTask}>
                <panels_1.PanelHeader>
                  Jobs Finished <small>{activeTask}</small>
                </panels_1.PanelHeader>
                <panels_1.PanelBody withPadding>
                  <internalStatChart_1.default since={this.state.since} resolution={this.state.resolution} stat={"jobs.finished." + activeTask} label="jobs" height={100}/>
                </panels_1.PanelBody>
              </panels_1.Panel>
            </div>) : null}
        </div>
      </div>);
    };
    return AdminQueue;
}(asyncView_1.default));
exports.default = AdminQueue;
var Header = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"])));
var templateObject_1;
//# sourceMappingURL=adminQueue.jsx.map