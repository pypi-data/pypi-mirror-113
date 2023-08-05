Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var clippedBox_1 = tslib_1.__importDefault(require("app/components/clippedBox"));
var contextBlock_1 = tslib_1.__importDefault(require("app/components/events/contexts/contextBlock"));
var locale_1 = require("app/locale");
var ReduxContextType = /** @class */ (function (_super) {
    tslib_1.__extends(ReduxContextType, _super);
    function ReduxContextType() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ReduxContextType.prototype.getKnownData = function () {
        return [
            {
                key: 'value',
                subject: locale_1.t('Latest State'),
                value: this.props.data,
            },
        ];
    };
    ReduxContextType.prototype.render = function () {
        return (<clippedBox_1.default clipHeight={250}>
        <contextBlock_1.default data={this.getKnownData()}/>
      </clippedBox_1.default>);
    };
    return ReduxContextType;
}(React.Component));
exports.default = ReduxContextType;
//# sourceMappingURL=redux.jsx.map