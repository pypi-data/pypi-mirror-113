Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var cspContent_1 = tslib_1.__importDefault(require("app/components/events/interfaces/cspContent"));
var cspHelp_1 = tslib_1.__importDefault(require("app/components/events/interfaces/cspHelp"));
var locale_1 = require("app/locale");
function getView(view, data) {
    switch (view) {
        case 'report':
            return <cspContent_1.default data={data}/>;
        case 'raw':
            return <pre>{JSON.stringify({ 'csp-report': data }, null, 2)}</pre>;
        case 'help':
            return <cspHelp_1.default data={data}/>;
        default:
            throw new TypeError("Invalid view: " + view);
    }
}
var CspInterface = /** @class */ (function (_super) {
    tslib_1.__extends(CspInterface, _super);
    function CspInterface() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { view: 'report' };
        _this.toggleView = function (value) {
            _this.setState({
                view: value,
            });
        };
        return _this;
    }
    CspInterface.prototype.render = function () {
        var view = this.state.view;
        var data = this.props.data;
        var cleanData = data.original_policy !== 'string'
            ? data
            : tslib_1.__assign(tslib_1.__assign({}, data), { 
                // Hide the report-uri since this is redundant and silly
                original_policy: data.original_policy.replace(/(;\s+)?report-uri [^;]+/, '') });
        var actions = (<buttonBar_1.default merged active={view}>
        <button_1.default barId="report" size="xsmall" onClick={this.toggleView.bind(this, 'report')}>
          {locale_1.t('Report')}
        </button_1.default>
        <button_1.default barId="raw" size="xsmall" onClick={this.toggleView.bind(this, 'raw')}>
          {locale_1.t('Raw')}
        </button_1.default>
        <button_1.default barId="help" size="xsmall" onClick={this.toggleView.bind(this, 'help')}>
          {locale_1.t('Help')}
        </button_1.default>
      </buttonBar_1.default>);
        var children = getView(view, cleanData);
        return (<eventDataSection_1.default type="csp" title={<h3>{locale_1.t('CSP Report')}</h3>} actions={actions} wrapTitle={false}>
        {children}
      </eventDataSection_1.default>);
    };
    return CspInterface;
}(react_1.Component));
exports.default = CspInterface;
//# sourceMappingURL=csp.jsx.map