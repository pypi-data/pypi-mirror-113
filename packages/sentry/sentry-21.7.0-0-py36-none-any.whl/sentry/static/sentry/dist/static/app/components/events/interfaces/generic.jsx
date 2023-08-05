Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var keyValueList_1 = tslib_1.__importDefault(require("app/components/events/interfaces/keyValueList"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var locale_1 = require("app/locale");
function getView(view, data) {
    switch (view) {
        case 'report':
            return (<keyValueList_1.default data={Object.entries(data).map(function (_a) {
                    var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
                    return ({
                        key: key,
                        value: value,
                        subject: key,
                        meta: metaProxy_1.getMeta(data, key),
                    });
                })} isContextData/>);
        case 'raw':
            return <pre>{JSON.stringify({ 'csp-report': data }, null, 2)}</pre>;
        default:
            throw new TypeError("Invalid view: " + view);
    }
}
var GenericInterface = /** @class */ (function (_super) {
    tslib_1.__extends(GenericInterface, _super);
    function GenericInterface() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            view: 'report',
            data: _this.props.data,
        };
        _this.toggleView = function (value) {
            _this.setState({
                view: value,
            });
        };
        return _this;
    }
    GenericInterface.prototype.render = function () {
        var _a = this.state, view = _a.view, data = _a.data;
        var type = this.props.type;
        var title = (<div>
        <buttonBar_1.default merged active={view}>
          <button_1.default barId="report" size="xsmall" onClick={this.toggleView.bind(this, 'report')}>
            {locale_1.t('Report')}
          </button_1.default>
          <button_1.default barId="raw" size="xsmall" onClick={this.toggleView.bind(this, 'raw')}>
            {locale_1.t('Raw')}
          </button_1.default>
        </buttonBar_1.default>
        <h3>{locale_1.t('Report')}</h3>
      </div>);
        var children = getView(view, data);
        return (<eventDataSection_1.default type={type} title={title} wrapTitle={false}>
        {children}
      </eventDataSection_1.default>);
    };
    return GenericInterface;
}(react_1.Component));
exports.default = GenericInterface;
//# sourceMappingURL=generic.jsx.map