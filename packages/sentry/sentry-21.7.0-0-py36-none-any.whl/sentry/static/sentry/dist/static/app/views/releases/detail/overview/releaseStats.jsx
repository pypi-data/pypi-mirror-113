Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var styles_1 = require("app/components/charts/styles");
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var deployBadge_1 = tslib_1.__importDefault(require("app/components/deployBadge"));
var globalSelectionLink_1 = tslib_1.__importDefault(require("app/components/globalSelectionLink"));
var notAvailable_1 = tslib_1.__importDefault(require("app/components/notAvailable"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var notAvailableMessages_1 = tslib_1.__importDefault(require("app/constants/notAvailableMessages"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var discoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/discoverQuery"));
var fields_1 = require("app/utils/discover/fields");
var data_1 = require("app/views/performance/data");
var sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
var crashFree_1 = tslib_1.__importDefault(require("../../list/crashFree"));
var releaseAdoption_1 = tslib_1.__importDefault(require("../../list/releaseAdoption"));
var utils_2 = require("../../list/utils");
var utils_3 = require("../../utils");
var utils_4 = require("../utils");
function ReleaseStats(_a) {
    var _b;
    var organization = _a.organization, release = _a.release, project = _a.project, location = _a.location, selection = _a.selection, isHealthLoading = _a.isHealthLoading, hasHealthData = _a.hasHealthData, getHealthData = _a.getHealthData;
    var lastDeploy = release.lastDeploy, dateCreated = release.dateCreated, version = release.version;
    var crashCount = getHealthData.getCrashCount(version, project.id, utils_2.DisplayOption.SESSIONS);
    var crashFreeSessions = getHealthData.getCrashFreeRate(version, project.id, utils_2.DisplayOption.SESSIONS);
    var crashFreeUsers = getHealthData.getCrashFreeRate(version, project.id, utils_2.DisplayOption.USERS);
    var get24hSessionCountByRelease = getHealthData.get24hCountByRelease(version, project.id, utils_2.DisplayOption.SESSIONS);
    var get24hSessionCountByProject = getHealthData.get24hCountByProject(project.id, utils_2.DisplayOption.SESSIONS);
    var get24hUserCountByRelease = getHealthData.get24hCountByRelease(version, project.id, utils_2.DisplayOption.USERS);
    var get24hUserCountByProject = getHealthData.get24hCountByProject(project.id, utils_2.DisplayOption.USERS);
    var sessionAdoption = getHealthData.getAdoption(version, project.id, utils_2.DisplayOption.SESSIONS);
    var userAdoption = getHealthData.getAdoption(version, project.id, utils_2.DisplayOption.USERS);
    var apdexField;
    var apdexPerformanceTerm;
    if (organization.features.includes('project-transaction-threshold')) {
        apdexPerformanceTerm = data_1.PERFORMANCE_TERM.APDEX_NEW;
        apdexField = 'apdex()';
    }
    else {
        apdexPerformanceTerm = data_1.PERFORMANCE_TERM.APDEX;
        apdexField = "apdex(" + organization.apdexThreshold + ")";
    }
    return (<Container>
      <div>
        <styles_1.SectionHeading>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? locale_1.t('Date Deployed') : locale_1.t('Date Created')}
        </styles_1.SectionHeading>
        <SectionContent>
          <timeSince_1.default date={(_b = lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) !== null && _b !== void 0 ? _b : dateCreated}/>
        </SectionContent>
      </div>

      <div>
        <styles_1.SectionHeading>{locale_1.t('Last Deploy')}</styles_1.SectionHeading>
        <SectionContent>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? (<deployBadge_1.default deploy={lastDeploy} orgSlug={organization.slug} version={version} projectId={project.id}/>) : (<notAvailable_1.default />)}
        </SectionContent>
      </div>

      {!organization.features.includes('release-comparison') && (<react_1.Fragment>
          <CrashFreeSection>
            <styles_1.SectionHeading>
              {locale_1.t('Crash Free Rate')}
              <questionTooltip_1.default position="top" title={sessionTerm_1.getSessionTermDescription(sessionTerm_1.SessionTerm.CRASH_FREE, project.platform)} size="sm"/>
            </styles_1.SectionHeading>
            {isHealthLoading ? (<placeholder_1.default height="58px"/>) : (<SectionContent>
                {utils_1.defined(crashFreeSessions) || utils_1.defined(crashFreeUsers) ? (<CrashFreeWrapper>
                    {utils_1.defined(crashFreeSessions) && (<div>
                        <crashFree_1.default percent={crashFreeSessions} iconSize="md" displayOption={utils_2.DisplayOption.SESSIONS}/>
                      </div>)}

                    {utils_1.defined(crashFreeUsers) && (<div>
                        <crashFree_1.default percent={crashFreeUsers} iconSize="md" displayOption={utils_2.DisplayOption.USERS}/>
                      </div>)}
                  </CrashFreeWrapper>) : (<notAvailable_1.default tooltip={notAvailableMessages_1.default.releaseHealth}/>)}
              </SectionContent>)}
          </CrashFreeSection>

          <AdoptionSection>
            <styles_1.SectionHeading>
              {locale_1.t('Adoption')}
              <questionTooltip_1.default position="top" title={sessionTerm_1.getSessionTermDescription(sessionTerm_1.SessionTerm.ADOPTION, project.platform)} size="sm"/>
            </styles_1.SectionHeading>
            {isHealthLoading ? (<placeholder_1.default height="88px"/>) : (<SectionContent>
                {get24hSessionCountByProject || get24hUserCountByProject ? (<AdoptionWrapper>
                    {utils_1.defined(get24hSessionCountByProject) &&
                        get24hSessionCountByProject > 0 && (<releaseAdoption_1.default releaseCount={get24hSessionCountByRelease !== null && get24hSessionCountByRelease !== void 0 ? get24hSessionCountByRelease : 0} projectCount={get24hSessionCountByProject !== null && get24hSessionCountByProject !== void 0 ? get24hSessionCountByProject : 0} adoption={sessionAdoption !== null && sessionAdoption !== void 0 ? sessionAdoption : 0} displayOption={utils_2.DisplayOption.SESSIONS} withLabels/>)}

                    {utils_1.defined(get24hUserCountByProject) &&
                        get24hUserCountByProject > 0 && (<releaseAdoption_1.default releaseCount={get24hUserCountByRelease !== null && get24hUserCountByRelease !== void 0 ? get24hUserCountByRelease : 0} projectCount={get24hUserCountByProject !== null && get24hUserCountByProject !== void 0 ? get24hUserCountByProject : 0} adoption={userAdoption !== null && userAdoption !== void 0 ? userAdoption : 0} displayOption={utils_2.DisplayOption.USERS} withLabels/>)}
                  </AdoptionWrapper>) : (<notAvailable_1.default tooltip={notAvailableMessages_1.default.releaseHealth}/>)}
              </SectionContent>)}
          </AdoptionSection>

          <LinkedStatsSection>
            <div>
              <styles_1.SectionHeading>{locale_1.t('New Issues')}</styles_1.SectionHeading>
              <SectionContent>
                <tooltip_1.default title={locale_1.t('Open in Issues')}>
                  <globalSelectionLink_1.default to={utils_3.getReleaseNewIssuesUrl(organization.slug, project.id, version)}>
                    <count_1.default value={project.newGroups}/>
                  </globalSelectionLink_1.default>
                </tooltip_1.default>
              </SectionContent>
            </div>

            <div>
              <styles_1.SectionHeading>
                {sessionTerm_1.sessionTerm.crashes}
                <questionTooltip_1.default position="top" title={sessionTerm_1.getSessionTermDescription(sessionTerm_1.SessionTerm.CRASHES, project.platform)} size="sm"/>
              </styles_1.SectionHeading>
              {isHealthLoading ? (<placeholder_1.default height="24px"/>) : (<SectionContent>
                  {hasHealthData ? (<tooltip_1.default title={locale_1.t('Open in Issues')}>
                      <globalSelectionLink_1.default to={utils_3.getReleaseUnhandledIssuesUrl(organization.slug, project.id, version)}>
                        <count_1.default value={crashCount !== null && crashCount !== void 0 ? crashCount : 0}/>
                      </globalSelectionLink_1.default>
                    </tooltip_1.default>) : (<notAvailable_1.default tooltip={notAvailableMessages_1.default.releaseHealth}/>)}
                </SectionContent>)}
            </div>

            <div>
              <styles_1.SectionHeading>
                {locale_1.t('Apdex')}
                <questionTooltip_1.default position="top" title={data_1.getTermHelp(organization, apdexPerformanceTerm)} size="sm"/>
              </styles_1.SectionHeading>
              <SectionContent>
                <feature_1.default features={['performance-view']}>
                  {function (hasFeature) {
                return hasFeature ? (<discoverQuery_1.default eventView={utils_4.getReleaseEventView(selection, release === null || release === void 0 ? void 0 : release.version, organization)} location={location} orgSlug={organization.slug}>
                        {function (_a) {
                        var isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData;
                        if (isLoading) {
                            return <placeholder_1.default height="24px"/>;
                        }
                        if (error || !tableData || tableData.data.length === 0) {
                            return <notAvailable_1.default />;
                        }
                        return (<globalSelectionLink_1.default to={{
                                pathname: "/organizations/" + organization.slug + "/performance/",
                                query: {
                                    query: "release:" + (release === null || release === void 0 ? void 0 : release.version),
                                },
                            }}>
                              <tooltip_1.default title={locale_1.t('Open in Performance')}>
                                <count_1.default value={tableData.data[0][fields_1.getAggregateAlias(apdexField)]}/>
                              </tooltip_1.default>
                            </globalSelectionLink_1.default>);
                    }}
                      </discoverQuery_1.default>) : (<notAvailable_1.default tooltip={notAvailableMessages_1.default.performance}/>);
            }}
                </feature_1.default>
              </SectionContent>
            </div>
          </LinkedStatsSection>
        </react_1.Fragment>)}
    </Container>);
}
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 50% 50%;\n  grid-row-gap: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 50% 50%;\n  grid-row-gap: ", ";\n  margin-bottom: ", ";\n"])), space_1.default(2), space_1.default(3));
var SectionContent = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject([""], [""])));
var CrashFreeSection = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  grid-column: 1/3;\n"], ["\n  grid-column: 1/3;\n"])));
var CrashFreeWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space_1.default(1));
var AdoptionSection = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  grid-column: 1/3;\n  margin-bottom: ", ";\n"], ["\n  grid-column: 1/3;\n  margin-bottom: ", ";\n"])), space_1.default(1));
var AdoptionWrapper = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space_1.default(1.5));
var LinkedStatsSection = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  grid-column: 1/3;\n  display: flex;\n  justify-content: space-between;\n"], ["\n  grid-column: 1/3;\n  display: flex;\n  justify-content: space-between;\n"])));
exports.default = ReleaseStats;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=releaseStats.jsx.map