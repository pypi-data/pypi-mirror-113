Object.defineProperty(exports, "__esModule", { value: true });
exports.OwnershipRules = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var sidebarSection_1 = tslib_1.__importDefault(require("../sidebarSection"));
var OwnershipRules = function (_a) {
    var project = _a.project, organization = _a.organization, issueId = _a.issueId;
    var handleOpenCreateOwnershipRule = function () {
        modal_1.openCreateOwnershipRule({ project: project, organization: organization, issueId: issueId });
    };
    return (<sidebarSection_1.default title={<react_1.Fragment>
          {locale_1.t('Ownership Rules')}
          <react_2.ClassNames>
            {function (_a) {
                var css = _a.css;
                return (<hovercard_1.default body={<HelpfulBody>
                    <p>
                      {locale_1.t('Ownership rules allow you to associate file paths and URLs to specific teams or users, so alerts can be routed to the right people.')}
                    </p>
                    <button_1.default href="https://docs.sentry.io/workflow/issue-owners/" priority="primary">
                      {locale_1.t('Learn more')}
                    </button_1.default>
                  </HelpfulBody>} containerClassName={css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n                  display: flex;\n                  align-items: center;\n                "], ["\n                  display: flex;\n                  align-items: center;\n                "])))}>
                <StyledIconQuestion size="xs"/>
              </hovercard_1.default>);
            }}
          </react_2.ClassNames>
        </react_1.Fragment>}>
      <guideAnchor_1.default target="owners" position="bottom" offset={space_1.default(3)}>
        <button_1.default onClick={handleOpenCreateOwnershipRule} size="small">
          {locale_1.t('Create Ownership Rule')}
        </button_1.default>
      </guideAnchor_1.default>
    </sidebarSection_1.default>);
};
exports.OwnershipRules = OwnershipRules;
var StyledIconQuestion = styled_1.default(icons_1.IconQuestion)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(0.5));
var HelpfulBody = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  text-align: center;\n"], ["\n  padding: ", ";\n  text-align: center;\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=ownershipRules.jsx.map