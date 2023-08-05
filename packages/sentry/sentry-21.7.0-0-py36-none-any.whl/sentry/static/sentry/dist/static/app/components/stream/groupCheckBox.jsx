Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var checkbox_1 = tslib_1.__importDefault(require("app/components/checkbox"));
var locale_1 = require("app/locale");
var selectedGroupStore_1 = tslib_1.__importDefault(require("app/stores/selectedGroupStore"));
var GroupCheckBox = /** @class */ (function (_super) {
    tslib_1.__extends(GroupCheckBox, _super);
    function GroupCheckBox() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isSelected: selectedGroupStore_1.default.isSelected(_this.props.id),
        };
        _this.unsubscribe = selectedGroupStore_1.default.listen(function () {
            _this.onSelectedGroupChange();
        }, undefined);
        _this.handleSelect = function () {
            var id = _this.props.id;
            selectedGroupStore_1.default.toggleSelect(id);
        };
        return _this;
    }
    GroupCheckBox.prototype.componentWillReceiveProps = function (nextProps) {
        if (nextProps.id !== this.props.id) {
            this.setState({
                isSelected: selectedGroupStore_1.default.isSelected(nextProps.id),
            });
        }
    };
    GroupCheckBox.prototype.shouldComponentUpdate = function (_nextProps, nextState) {
        return nextState.isSelected !== this.state.isSelected;
    };
    GroupCheckBox.prototype.componentWillUnmount = function () {
        this.unsubscribe();
    };
    GroupCheckBox.prototype.onSelectedGroupChange = function () {
        var isSelected = selectedGroupStore_1.default.isSelected(this.props.id);
        if (isSelected !== this.state.isSelected) {
            this.setState({
                isSelected: isSelected,
            });
        }
    };
    GroupCheckBox.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, id = _a.id;
        var isSelected = this.state.isSelected;
        return (<checkbox_1.default aria-label={locale_1.t('Select Issue')} value={id} checked={isSelected} onChange={this.handleSelect} disabled={disabled}/>);
    };
    return GroupCheckBox;
}(react_1.Component));
exports.default = GroupCheckBox;
//# sourceMappingURL=groupCheckBox.jsx.map