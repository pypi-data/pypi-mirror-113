Object.defineProperty(exports, "__esModule", { value: true });
exports.TextOverflow = exports.GetStarted = exports.DeployRows = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
exports.TextOverflow = textOverflow_1.default;
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var DEPLOY_COUNT = 2;
var Deploys = function (_a) {
    var project = _a.project, shorten = _a.shorten;
    var flattenedDeploys = Object.entries(project.latestDeploys || {}).map(function (_a) {
        var _b = tslib_1.__read(_a, 2), environment = _b[0], value = _b[1];
        return (tslib_1.__assign({ environment: environment }, value));
    });
    var deploys = (flattenedDeploys || [])
        .sort(function (a, b) { return new Date(b.dateFinished).getTime() - new Date(a.dateFinished).getTime(); })
        .slice(0, DEPLOY_COUNT);
    if (!deploys.length) {
        return <NoDeploys />;
    }
    return (<DeployRows>
      {deploys.map(function (deploy) { return (<Deploy key={deploy.environment + "-" + deploy.version} deploy={deploy} project={project} shorten={shorten}/>); })}
    </DeployRows>);
};
exports.default = Deploys;
var Deploy = function (_a) {
    var deploy = _a.deploy, project = _a.project, shorten = _a.shorten;
    return (<react_1.Fragment>
    <icons_1.IconReleases size="sm"/>
    <textOverflow_1.default>
      <Environment>{deploy.environment}</Environment>
      <version_1.default version={deploy.version} projectId={project.id} tooltipRawVersion truncate/>
    </textOverflow_1.default>

    <DeployTime>
      {getDynamicText_1.default({
            fixed: '3 hours ago',
            value: (<timeSince_1.default date={deploy.dateFinished} shorten={shorten ? shorten : false}/>),
        })}
    </DeployTime>
  </react_1.Fragment>);
};
var NoDeploys = function () { return (<GetStarted>
    <button_1.default size="small" href="https://docs.sentry.io/product/releases/" external>
      {locale_1.t('Track Deploys')}
    </button_1.default>
  </GetStarted>); };
var DeployContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  height: 115px;\n"], ["\n  padding: ", ";\n  height: 115px;\n"])), space_1.default(2));
var DeployRows = styled_1.default(DeployContainer)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 30px 1fr 1fr;\n  grid-template-rows: auto;\n  grid-column-gap: ", ";\n  grid-row-gap: ", ";\n  font-size: ", ";\n  line-height: 1.2;\n"], ["\n  display: grid;\n  grid-template-columns: 30px 1fr 1fr;\n  grid-template-rows: auto;\n  grid-column-gap: ", ";\n  grid-row-gap: ", ";\n  font-size: ", ";\n  line-height: 1.2;\n"])), space_1.default(1), space_1.default(1), function (p) { return p.theme.fontSizeMedium; });
exports.DeployRows = DeployRows;
var Environment = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin: 0;\n"], ["\n  color: ", ";\n  margin: 0;\n"])), function (p) { return p.theme.textColor; });
var DeployTime = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  overflow: hidden;\n  text-align: right;\n  text-overflow: ellipsis;\n"], ["\n  color: ", ";\n  overflow: hidden;\n  text-align: right;\n  text-overflow: ellipsis;\n"])), function (p) { return p.theme.gray300; });
var GetStarted = styled_1.default(DeployContainer)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])));
exports.GetStarted = GetStarted;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=deploys.jsx.map