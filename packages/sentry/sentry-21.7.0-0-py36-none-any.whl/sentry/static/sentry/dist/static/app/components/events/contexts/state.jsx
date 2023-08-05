Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var upperFirst_1 = tslib_1.__importDefault(require("lodash/upperFirst"));
var clippedBox_1 = tslib_1.__importDefault(require("app/components/clippedBox"));
var contextBlock_1 = tslib_1.__importDefault(require("app/components/events/contexts/contextBlock"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var locale_1 = require("app/locale");
var StateContextType = /** @class */ (function (_super) {
    tslib_1.__extends(StateContextType, _super);
    function StateContextType() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    StateContextType.prototype.getStateTitle = function (name, type) {
        return "" + name + (type ? " (" + upperFirst_1.default(type) + ")" : '');
    };
    StateContextType.prototype.getKnownData = function () {
        var primaryState = this.props.data.state;
        if (!primaryState) {
            return [];
        }
        return [
            {
                key: 'state',
                subject: this.getStateTitle(locale_1.t('State'), primaryState.type),
                value: primaryState.value,
            },
        ];
    };
    StateContextType.prototype.getUnknownData = function () {
        var _this = this;
        var data = this.props.data;
        return Object.entries(data)
            .filter(function (_a) {
            var _b = tslib_1.__read(_a, 1), key = _b[0];
            return !['type', 'title', 'state'].includes(key);
        })
            .map(function (_a) {
            var _b = tslib_1.__read(_a, 2), name = _b[0], state = _b[1];
            return ({
                key: name,
                value: state.value,
                subject: _this.getStateTitle(name, state.type),
                meta: metaProxy_1.getMeta(data, name),
            });
        });
    };
    StateContextType.prototype.render = function () {
        return (<clippedBox_1.default clipHeight={250}>
        <contextBlock_1.default data={this.getKnownData()}/>
        <contextBlock_1.default data={this.getUnknownData()}/>
      </clippedBox_1.default>);
    };
    return StateContextType;
}(React.Component));
exports.default = StateContextType;
//# sourceMappingURL=state.jsx.map