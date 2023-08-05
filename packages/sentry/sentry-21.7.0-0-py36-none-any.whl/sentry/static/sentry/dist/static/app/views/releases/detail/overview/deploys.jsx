Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var deployBadge_1 = tslib_1.__importDefault(require("app/components/deployBadge"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var styles_1 = require("./styles");
var Deploys = function (_a) {
    var version = _a.version, orgSlug = _a.orgSlug, projectId = _a.projectId, deploys = _a.deploys;
    return (<styles_1.Wrapper>
      <styles_1.SectionHeading>{locale_1.t('Deploys')}</styles_1.SectionHeading>

      {deploys.map(function (deploy) { return (<Row key={deploy.id}>
          <StyledDeployBadge deploy={deploy} orgSlug={orgSlug} version={version} projectId={projectId}/>
          <textOverflow_1.default>
            <timeSince_1.default date={deploy.dateFinished}/>
          </textOverflow_1.default>
        </Row>); })}
    </styles_1.Wrapper>);
};
var Row = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  font-size: ", ";\n  color: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  font-size: ", ";\n  color: ", ";\n"])), space_1.default(1), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; });
var StyledDeployBadge = styled_1.default(deployBadge_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
exports.default = Deploys;
var templateObject_1, templateObject_2;
//# sourceMappingURL=deploys.jsx.map