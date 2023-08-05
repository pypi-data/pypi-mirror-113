Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var iconGrabbable_1 = require("app/icons/iconGrabbable");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("../utils");
var actions_1 = tslib_1.__importDefault(require("./actions"));
var conditions_1 = tslib_1.__importDefault(require("./conditions"));
var sampleRate_1 = tslib_1.__importDefault(require("./sampleRate"));
var type_1 = tslib_1.__importDefault(require("./type"));
var Rule = /** @class */ (function (_super) {
    tslib_1.__extends(Rule, _super);
    function Rule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isMenuActionsOpen: false,
        };
        _this.handleChangeMenuAction = function () {
            _this.setState(function (state) { return ({
                isMenuActionsOpen: !state.isMenuActionsOpen,
            }); });
        };
        return _this;
    }
    Rule.prototype.componentDidMount = function () {
        this.checkMenuActionsVisibility();
    };
    Rule.prototype.componentDidUpdate = function () {
        this.checkMenuActionsVisibility();
    };
    Rule.prototype.checkMenuActionsVisibility = function () {
        var _a = this.props, dragging = _a.dragging, sorting = _a.sorting;
        var isMenuActionsOpen = this.state.isMenuActionsOpen;
        if ((dragging || sorting) && isMenuActionsOpen) {
            this.setState({ isMenuActionsOpen: false });
        }
    };
    Rule.prototype.render = function () {
        var _a = this.props, rule = _a.rule, onEditRule = _a.onEditRule, onDeleteRule = _a.onDeleteRule, disabled = _a.disabled, listeners = _a.listeners, grabAttributes = _a.grabAttributes;
        var type = rule.type, condition = rule.condition, sampleRate = rule.sampleRate;
        var isMenuActionsOpen = this.state.isMenuActionsOpen;
        return (<Columns>
        <GrabColumn>
          <tooltip_1.default title={disabled
                ? locale_1.t('You do not have permission to reorder dynamic sampling rules.')
                : undefined}>
            <IconGrabbableWrapper {...listeners} disabled={disabled} {...grabAttributes}>
              <iconGrabbable_1.IconGrabbable />
            </IconGrabbableWrapper>
          </tooltip_1.default>
        </GrabColumn>
        <Column>
          <type_1.default type={type}/>
        </Column>
        <Column>
          <conditions_1.default condition={condition}/>
        </Column>
        <CenteredColumn>
          <sampleRate_1.default sampleRate={sampleRate}/>
        </CenteredColumn>
        <Column>
          <actions_1.default onEditRule={onEditRule} onDeleteRule={onDeleteRule} disabled={disabled} onOpenMenuActions={this.handleChangeMenuAction} isMenuActionsOpen={isMenuActionsOpen}/>
        </Column>
      </Columns>);
    };
    return Rule;
}(react_1.Component));
exports.default = Rule;
var Columns = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  ", "\n  > * {\n    overflow: visible;\n    :nth-child(5n) {\n      justify-content: flex-end;\n    }\n  }\n"], ["\n  display: grid;\n  align-items: center;\n  ", "\n  > * {\n    overflow: visible;\n    :nth-child(5n) {\n      justify-content: flex-end;\n    }\n  }\n"])), function (p) { return utils_1.layout(p.theme); });
var Column = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n  cursor: default;\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n  cursor: default;\n"])), space_1.default(2));
var GrabColumn = styled_1.default(Column)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  cursor: inherit;\n  [role='button'] {\n    cursor: grab;\n  }\n"], ["\n  cursor: inherit;\n  [role='button'] {\n    cursor: grab;\n  }\n"])));
var CenteredColumn = styled_1.default(Column)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  text-align: center;\n  justify-content: center;\n"], ["\n  text-align: center;\n  justify-content: center;\n"])));
var IconGrabbableWrapper = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", ";\n  outline: none;\n"], ["\n  ", ";\n  outline: none;\n"])), function (p) {
    return p.disabled &&
        "\n    color: " + p.theme.disabled + ";\n    cursor: not-allowed;\n  ";
});
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map