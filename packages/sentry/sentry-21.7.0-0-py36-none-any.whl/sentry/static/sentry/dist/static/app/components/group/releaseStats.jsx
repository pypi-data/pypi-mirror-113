Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var releaseChart_1 = tslib_1.__importDefault(require("app/components/group/releaseChart"));
var seenInfo_1 = tslib_1.__importDefault(require("app/components/group/seenInfo"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var sidebarSection_1 = tslib_1.__importDefault(require("./sidebarSection"));
var GroupReleaseStats = function (_a) {
    var organization = _a.organization, project = _a.project, environments = _a.environments, allEnvironments = _a.allEnvironments, group = _a.group, currentRelease = _a.currentRelease;
    var environmentLabel = environments.length > 0
        ? environments.map(function (env) { return env.displayName; }).join(', ')
        : locale_1.t('All Environments');
    var shortEnvironmentLabel = environments.length > 1
        ? locale_1.t('selected environments')
        : environments.length === 1
            ? environments[0].displayName
            : undefined;
    var projectId = project.id;
    var projectSlug = project.slug;
    var hasRelease = new Set(project.features).has('releases');
    var releaseTrackingUrl = "/settings/" + organization.slug + "/projects/" + project.slug + "/release-tracking/";
    return (<sidebarSection_1.default title={<span data-test-id="env-label">{environmentLabel}</span>}>
      {!group || !allEnvironments ? (<placeholder_1.default height="288px"/>) : (<react_1.Fragment>
          <releaseChart_1.default group={allEnvironments} environment={environmentLabel} environmentStats={group.stats} release={currentRelease === null || currentRelease === void 0 ? void 0 : currentRelease.release} releaseStats={currentRelease === null || currentRelease === void 0 ? void 0 : currentRelease.stats} statsPeriod="24h" title={locale_1.t('Last 24 Hours')} firstSeen={group.firstSeen} lastSeen={group.lastSeen}/>
          <releaseChart_1.default group={allEnvironments} environment={environmentLabel} environmentStats={group.stats} release={currentRelease === null || currentRelease === void 0 ? void 0 : currentRelease.release} releaseStats={currentRelease === null || currentRelease === void 0 ? void 0 : currentRelease.stats} statsPeriod="30d" title={locale_1.t('Last 30 Days')} className="bar-chart-small" firstSeen={group.firstSeen} lastSeen={group.lastSeen}/>

          <sidebarSection_1.default secondary title={<span>
                {locale_1.t('Last seen')}
                <TooltipWrapper>
                  <tooltip_1.default title={locale_1.t('When the most recent event in this issue was captured.')} disableForVisualTest>
                    <StyledIconQuest size="xs" color="gray200"/>
                  </tooltip_1.default>
                </TooltipWrapper>
              </span>}>
            <seenInfo_1.default organization={organization} projectId={projectId} projectSlug={projectSlug} date={getDynamicText_1.default({
                value: group.lastSeen,
                fixed: '2016-01-13T03:08:25Z',
            })} dateGlobal={allEnvironments.lastSeen} hasRelease={hasRelease} environment={shortEnvironmentLabel} release={group.lastRelease || null} title={locale_1.t('Last seen')}/>
          </sidebarSection_1.default>

          <sidebarSection_1.default secondary title={<span>
                {locale_1.t('First seen')}
                <TooltipWrapper>
                  <tooltip_1.default title={locale_1.t('When the first event in this issue was captured.')} disableForVisualTest>
                    <StyledIconQuest size="xs" color="gray200"/>
                  </tooltip_1.default>
                </TooltipWrapper>
              </span>}>
            <seenInfo_1.default organization={organization} projectId={projectId} projectSlug={projectSlug} date={getDynamicText_1.default({
                value: group.firstSeen,
                fixed: '2015-08-13T03:08:25Z',
            })} dateGlobal={allEnvironments.firstSeen} hasRelease={hasRelease} environment={shortEnvironmentLabel} release={group.firstRelease || null} title={locale_1.t('First seen')}/>
          </sidebarSection_1.default>
          {!hasRelease ? (<sidebarSection_1.default secondary title={locale_1.t('Releases not configured')}>
              <a href={releaseTrackingUrl}>{locale_1.t('Setup Releases')}</a>{' '}
              {locale_1.t(' to make issues easier to fix.')}
            </sidebarSection_1.default>) : null}
        </react_1.Fragment>)}
    </sidebarSection_1.default>);
};
exports.default = react_1.memo(GroupReleaseStats);
var TooltipWrapper = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(0.5));
var StyledIconQuest = styled_1.default(icons_1.IconQuestion)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  top: 2px;\n"], ["\n  position: relative;\n  top: 2px;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=releaseStats.jsx.map