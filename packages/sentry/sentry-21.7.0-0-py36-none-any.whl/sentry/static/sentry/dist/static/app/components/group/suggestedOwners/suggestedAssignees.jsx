Object.defineProperty(exports, "__esModule", { value: true });
exports.SuggestedAssignees = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var actorAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/actorAvatar"));
var suggestedOwnerHovercard_1 = tslib_1.__importDefault(require("app/components/group/suggestedOwnerHovercard"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var sidebarSection_1 = tslib_1.__importDefault(require("../sidebarSection"));
var SuggestedAssignees = function (_a) {
    var owners = _a.owners, onAssign = _a.onAssign;
    return (<sidebarSection_1.default title={<react_1.Fragment>
        {locale_1.t('Suggested Assignees')}
        <Subheading>{locale_1.t('Click to assign')}</Subheading>
      </react_1.Fragment>}>
    <Content>
      {owners.map(function (owner, i) { return (<suggestedOwnerHovercard_1.default key={owner.actor.id + ":" + owner.actor.email + ":" + owner.actor.name + ":" + i} {...owner}>
          <actorAvatar_1.default css={react_2.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n              cursor: pointer;\n            "], ["\n              cursor: pointer;\n            "])))} onClick={onAssign(owner.actor)} hasTooltip={false} actor={owner.actor}/>
        </suggestedOwnerHovercard_1.default>); })}
    </Content>
  </sidebarSection_1.default>);
};
exports.SuggestedAssignees = SuggestedAssignees;
var Subheading = styled_1.default('small')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  line-height: 100%;\n  font-weight: 400;\n  margin-left: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n  line-height: 100%;\n  font-weight: 400;\n  margin-left: ", ";\n"])), function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.theme.gray300; }, space_1.default(0.5));
var Content = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: repeat(auto-fill, 20px);\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: repeat(auto-fill, 20px);\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=suggestedAssignees.jsx.map