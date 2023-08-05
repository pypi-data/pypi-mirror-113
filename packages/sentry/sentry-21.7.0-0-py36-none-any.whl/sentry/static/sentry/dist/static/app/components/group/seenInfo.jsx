Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var hovercard_1 = require("app/components/hovercard");
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var versionHoverCard_1 = tslib_1.__importDefault(require("app/components/versionHoverCard"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var SeenInfo = /** @class */ (function (_super) {
    tslib_1.__extends(SeenInfo, _super);
    function SeenInfo() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SeenInfo.prototype.shouldComponentUpdate = function (nextProps) {
        var _a;
        var _b = this.props, date = _b.date, release = _b.release;
        return (release === null || release === void 0 ? void 0 : release.version) !== ((_a = nextProps.release) === null || _a === void 0 ? void 0 : _a.version) || date !== nextProps.date;
    };
    SeenInfo.prototype.getReleaseTrackingUrl = function () {
        var _a = this.props, organization = _a.organization, projectSlug = _a.projectSlug;
        var orgSlug = organization.slug;
        return "/settings/" + orgSlug + "/projects/" + projectSlug + "/release-tracking/";
    };
    SeenInfo.prototype.render = function () {
        var _a = this.props, date = _a.date, dateGlobal = _a.dateGlobal, environment = _a.environment, release = _a.release, organization = _a.organization, projectSlug = _a.projectSlug, projectId = _a.projectId;
        return (<HovercardWrapper>
        <StyledHovercard header={<div>
              <TimeSinceWrapper>
                {locale_1.t('Any Environment')}
                <timeSince_1.default date={dateGlobal} disabledAbsoluteTooltip/>
              </TimeSinceWrapper>
              {environment && (<TimeSinceWrapper>
                  {utils_1.toTitleCase(environment)}
                  {date ? (<timeSince_1.default date={date} disabledAbsoluteTooltip/>) : (<span>{locale_1.t('N/A')}</span>)}
                </TimeSinceWrapper>)}
            </div>} body={date ? (<StyledDateTime date={date}/>) : (<NoEnvironment>{locale_1.t("N/A for " + environment)}</NoEnvironment>)} position="top" tipColor={theme_1.default.gray500}>
          <DateWrapper>
            {date ? (<TooltipWrapper>
                <StyledTimeSince date={date} disabledAbsoluteTooltip/>
              </TooltipWrapper>) : dateGlobal && environment === '' ? (<React.Fragment>
                <timeSince_1.default date={dateGlobal} disabledAbsoluteTooltip/>
                <StyledTimeSince date={dateGlobal} disabledAbsoluteTooltip/>
              </React.Fragment>) : (<NoDateTime>{locale_1.t('N/A')}</NoDateTime>)}
          </DateWrapper>
        </StyledHovercard>
        <DateWrapper>
          {utils_1.defined(release) ? (<React.Fragment>
              {locale_1.t('in release ')}
              <versionHoverCard_1.default organization={organization} projectSlug={projectSlug} releaseVersion={release.version}>
                <span>
                  <version_1.default version={release.version} projectId={projectId}/>
                </span>
              </versionHoverCard_1.default>
            </React.Fragment>) : null}
        </DateWrapper>
      </HovercardWrapper>);
    };
    return SeenInfo;
}(React.Component));
var dateTimeCss = function (p) { return react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  display: flex;\n  justify-content: center;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  display: flex;\n  justify-content: center;\n"])), p.theme.gray300, p.theme.fontSizeMedium); };
var HovercardWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var DateWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  ", ";\n"], ["\n  margin-bottom: ", ";\n  ", ";\n"])), space_1.default(2), overflowEllipsis_1.default);
var StyledDateTime = styled_1.default(dateTime_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), dateTimeCss);
var NoEnvironment = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), dateTimeCss);
var NoDateTime = styled_1.default('span')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(0.5));
var TooltipWrapper = styled_1.default('span')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n  svg {\n    margin-right: ", ";\n    position: relative;\n    top: 1px;\n  }\n"], ["\n  margin-right: ", ";\n  svg {\n    margin-right: ", ";\n    position: relative;\n    top: 1px;\n  }\n"])), space_1.default(0.25), space_1.default(0.5));
var TimeSinceWrapper = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n  display: flex;\n  justify-content: space-between;\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n  display: flex;\n  justify-content: space-between;\n"])), function (p) { return p.theme.fontSizeSmall; }, space_1.default(0.5));
var StyledTimeSince = styled_1.default(timeSince_1.default)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var StyledHovercard = styled_1.default(hovercard_1.Hovercard)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  width: 250px;\n  font-weight: normal;\n  border: 1px solid ", ";\n  background: ", ";\n  ", " {\n    font-weight: normal;\n    color: ", ";\n    background: ", ";\n    border-bottom: 1px solid ", ";\n  }\n  ", " {\n    padding: ", ";\n  }\n"], ["\n  width: 250px;\n  font-weight: normal;\n  border: 1px solid ", ";\n  background: ", ";\n  ", " {\n    font-weight: normal;\n    color: ", ";\n    background: ", ";\n    border-bottom: 1px solid ", ";\n  }\n  ", " {\n    padding: ", ";\n  }\n"])), function (p) { return p.theme.gray500; }, function (p) { return p.theme.gray500; }, hovercard_1.Header, function (p) { return p.theme.white; }, function (p) { return p.theme.gray500; }, function (p) { return p.theme.gray400; }, hovercard_1.Body, space_1.default(1.5));
exports.default = SeenInfo;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=seenInfo.jsx.map