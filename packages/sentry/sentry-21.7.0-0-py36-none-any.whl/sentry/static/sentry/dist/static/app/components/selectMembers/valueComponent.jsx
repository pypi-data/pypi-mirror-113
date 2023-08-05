Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var actorAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/actorAvatar"));
var ValueComponent = /** @class */ (function (_super) {
    tslib_1.__extends(ValueComponent, _super);
    function ValueComponent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleClick = function () {
            _this.props.onRemove(_this.props.value);
        };
        return _this;
    }
    ValueComponent.prototype.render = function () {
        return (<a onClick={this.handleClick}>
        <actorAvatar_1.default actor={this.props.value.actor} size={28}/>
      </a>);
    };
    return ValueComponent;
}(react_1.Component));
exports.default = ValueComponent;
//# sourceMappingURL=valueComponent.jsx.map