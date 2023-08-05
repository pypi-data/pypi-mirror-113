Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var dropdownAutoComplete_1 = tslib_1.__importDefault(require("app/components/dropdownAutoComplete"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var _1 = require(".");
var GroupingConfigSelect = /** @class */ (function (_super) {
    tslib_1.__extends(GroupingConfigSelect, _super);
    function GroupingConfigSelect() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GroupingConfigSelect.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { configs: [] });
    };
    GroupingConfigSelect.prototype.getEndpoints = function () {
        return [['configs', '/grouping-configs/']];
    };
    GroupingConfigSelect.prototype.renderLoading = function () {
        return this.renderBody();
    };
    GroupingConfigSelect.prototype.renderBody = function () {
        var _a = this.props, configId = _a.configId, eventConfigId = _a.eventConfigId, onSelect = _a.onSelect;
        var configs = this.state.configs;
        var options = configs.map(function (_a) {
            var id = _a.id, hidden = _a.hidden;
            return ({
                value: id,
                label: (<_1.GroupingConfigItem isHidden={hidden} isActive={id === eventConfigId}>
          {id}
        </_1.GroupingConfigItem>),
            });
        });
        return (<dropdownAutoComplete_1.default onSelect={onSelect} items={options}>
        {function (_a) {
                var isOpen = _a.isOpen;
                return (<tooltip_1.default title={locale_1.t('Click here to experiment with other grouping configs')}>
            <StyledDropdownButton isOpen={isOpen} size="small">
              <_1.GroupingConfigItem isActive={eventConfigId === configId}>
                {configId}
              </_1.GroupingConfigItem>
            </StyledDropdownButton>
          </tooltip_1.default>);
            }}
      </dropdownAutoComplete_1.default>);
    };
    return GroupingConfigSelect;
}(asyncComponent_1.default));
var StyledDropdownButton = styled_1.default(dropdownButton_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-weight: inherit;\n"], ["\n  font-weight: inherit;\n"])));
exports.default = GroupingConfigSelect;
var templateObject_1;
//# sourceMappingURL=groupingConfigSelect.jsx.map