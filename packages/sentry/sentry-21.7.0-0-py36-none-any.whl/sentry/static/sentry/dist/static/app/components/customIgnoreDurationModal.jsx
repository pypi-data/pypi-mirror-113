Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var moment_1 = tslib_1.__importDefault(require("moment"));
var sprintf_js_1 = require("sprintf-js");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var defaultProps = {
    label: locale_1.t('Ignore this issue until \u2026'),
};
var CustomIgnoreDurationModal = /** @class */ (function (_super) {
    tslib_1.__extends(CustomIgnoreDurationModal, _super);
    function CustomIgnoreDurationModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            dateWarning: false,
        };
        _this.snoozeDateInputRef = react_1.createRef();
        _this.snoozeTimeInputRef = react_1.createRef();
        _this.selectedIgnoreMinutes = function () {
            var _a, _b;
            var dateStr = (_a = _this.snoozeDateInputRef.current) === null || _a === void 0 ? void 0 : _a.value; // YYYY-MM-DD
            var timeStr = (_b = _this.snoozeTimeInputRef.current) === null || _b === void 0 ? void 0 : _b.value; // HH:MM
            if (dateStr && timeStr) {
                var selectedDate = moment_1.default.utc(dateStr + ' ' + timeStr);
                if (selectedDate.isValid()) {
                    var now = moment_1.default.utc();
                    return selectedDate.diff(now, 'minutes');
                }
            }
            return 0;
        };
        _this.snoozeClicked = function () {
            var minutes = _this.selectedIgnoreMinutes();
            _this.setState({
                dateWarning: minutes <= 0,
            });
            if (minutes > 0) {
                _this.props.onSelected({ ignoreDuration: minutes });
            }
            _this.props.closeModal();
        };
        return _this;
    }
    CustomIgnoreDurationModal.prototype.render = function () {
        // Give the user a sane starting point to select a date
        // (prettier than the empty date/time inputs):
        var defaultDate = new Date();
        defaultDate.setDate(defaultDate.getDate() + 14);
        defaultDate.setSeconds(0);
        defaultDate.setMilliseconds(0);
        var defaultDateVal = sprintf_js_1.sprintf('%d-%02d-%02d', defaultDate.getUTCFullYear(), defaultDate.getUTCMonth() + 1, defaultDate.getUTCDate());
        var defaultTimeVal = sprintf_js_1.sprintf('%02d:00', defaultDate.getUTCHours());
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, label = _a.label;
        return (<react_1.Fragment>
        <Header>{label}</Header>
        <Body>
          <form className="form-horizontal">
            <div className="control-group">
              <h6 className="nav-header">{locale_1.t('Date')}</h6>
              <input className="form-control" type="date" id="snooze-until-date" defaultValue={defaultDateVal} ref={this.snoozeDateInputRef} required style={{ padding: '0 10px' }}/>
            </div>
            <div className="control-group m-b-1">
              <h6 className="nav-header">{locale_1.t('Time (UTC)')}</h6>
              <input className="form-control" type="time" id="snooze-until-time" defaultValue={defaultTimeVal} ref={this.snoozeTimeInputRef} style={{ padding: '0 10px' }} required/>
            </div>
          </form>
        </Body>
        {this.state.dateWarning && (<alert_1.default icon={<icons_1.IconWarning size="md"/>} type="error">
            {locale_1.t('Please enter a valid date in the future')}
          </alert_1.default>)}
        <Footer>
          <buttonBar_1.default gap={1}>
            <button_1.default type="button" priority="default" onClick={this.props.closeModal}>
              {locale_1.t('Cancel')}
            </button_1.default>
            <button_1.default type="button" priority="primary" onClick={this.snoozeClicked}>
              {locale_1.t('Ignore')}
            </button_1.default>
          </buttonBar_1.default>
        </Footer>
      </react_1.Fragment>);
    };
    CustomIgnoreDurationModal.defaultProps = defaultProps;
    return CustomIgnoreDurationModal;
}(react_1.Component));
exports.default = CustomIgnoreDurationModal;
//# sourceMappingURL=customIgnoreDurationModal.jsx.map