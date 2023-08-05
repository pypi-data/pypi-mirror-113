Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var groupBy_1 = tslib_1.__importDefault(require("lodash/groupBy"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getSdkUpdateSuggestion_1 = tslib_1.__importDefault(require("app/utils/getSdkUpdateSuggestion"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var withSdkUpdates_1 = tslib_1.__importDefault(require("app/utils/withSdkUpdates"));
var collapsible_1 = tslib_1.__importDefault(require("../collapsible"));
var list_1 = tslib_1.__importDefault(require("../list"));
var listItem_1 = tslib_1.__importDefault(require("../list/listItem"));
var sidebarPanelItem_1 = tslib_1.__importDefault(require("./sidebarPanelItem"));
var flattenSuggestions = function (list) {
    return list.reduce(function (suggestions, sdk) { return tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(suggestions)), tslib_1.__read(sdk.suggestions)); }, []);
};
var BroadcastSdkUpdates = function (_a) {
    var projects = _a.projects, sdkUpdates = _a.sdkUpdates;
    if (!sdkUpdates) {
        return null;
    }
    // Are there any updates?
    if (flattenSuggestions(sdkUpdates).length === 0) {
        return null;
    }
    // Group SDK updates by project
    var items = Object.entries(groupBy_1.default(sdkUpdates, 'projectId'));
    return (<sidebarPanelItem_1.default hasSeen title={locale_1.t('Update your SDKs')} message={locale_1.t('We recommend updating the following SDKs to make sure you’re getting all the data you need.')}>
      <UpdatesList>
        <collapsible_1.default>
          {items.map(function (_a) {
            var _b = tslib_1.__read(_a, 2), projectId = _b[0], updates = _b[1];
            var project = projects.find(function (p) { return p.id === projectId; });
            if (project === undefined) {
                return null;
            }
            return (<div key={project.id}>
                <SdkProjectBadge project={project}/>
                <Suggestions>
                  {updates.map(function (sdkUpdate) { return (<div key={sdkUpdate.sdkName}>
                      <SdkName>
                        {sdkUpdate.sdkName}{' '}
                        <SdkOutdatedVersion>@v{sdkUpdate.sdkVersion}</SdkOutdatedVersion>
                      </SdkName>
                      <list_1.default>
                        {sdkUpdate.suggestions.map(function (suggestion, i) { return (<listItem_1.default key={i}>
                            {getSdkUpdateSuggestion_1.default({
                            sdk: {
                                name: sdkUpdate.sdkName,
                                version: sdkUpdate.sdkVersion,
                            },
                            suggestion: suggestion,
                            shortStyle: true,
                            capitalized: true,
                        })}
                          </listItem_1.default>); })}
                      </list_1.default>
                    </div>); })}
                </Suggestions>
              </div>);
        })}
        </collapsible_1.default>
      </UpdatesList>
    </sidebarPanelItem_1.default>);
};
var UpdatesList = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  display: grid;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n"], ["\n  margin-top: ", ";\n  display: grid;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n"])), space_1.default(3), space_1.default(3));
var Suggestions = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  margin-left: calc(", " + ", ");\n  display: grid;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n"], ["\n  margin-top: ", ";\n  margin-left: calc(", " + ", ");\n  display: grid;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n"])), space_1.default(1), space_1.default(4), space_1.default(0.25), space_1.default(1.5));
var SdkProjectBadge = styled_1.default(projectBadge_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var SdkName = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-family: ", ";\n  font-weight: bold;\n  margin-bottom: ", ";\n"], ["\n  font-family: ", ";\n  font-weight: bold;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.text.familyMono; }, space_1.default(1));
var SdkOutdatedVersion = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
exports.default = withSdkUpdates_1.default(withProjects_1.default(BroadcastSdkUpdates));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=broadcastSdkUpdates.jsx.map