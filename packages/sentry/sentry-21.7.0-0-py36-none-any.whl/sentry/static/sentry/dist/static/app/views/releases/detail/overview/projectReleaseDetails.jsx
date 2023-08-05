Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var keyValueTable_1 = require("app/components/keyValueTable");
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var locale_1 = require("app/locale");
var styles_1 = require("./styles");
var ProjectReleaseDetails = function (_a) {
    var _b;
    var release = _a.release, releaseMeta = _a.releaseMeta, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug;
    var version = release.version, versionInfo = release.versionInfo, dateCreated = release.dateCreated, firstEvent = release.firstEvent, lastEvent = release.lastEvent;
    return (<styles_1.Wrapper>
      <styles_1.SectionHeading>{locale_1.t('Project Release Details')}</styles_1.SectionHeading>
      <keyValueTable_1.KeyValueTable>
        <keyValueTable_1.KeyValueTableRow keyName={locale_1.t('Created')} value={<dateTime_1.default date={dateCreated} seconds={false}/>}/>
        <keyValueTable_1.KeyValueTableRow keyName={locale_1.t('Version')} value={<version_1.default version={version} anchor={false}/>}/>
        <keyValueTable_1.KeyValueTableRow keyName={locale_1.t('Package')} value={<StyledTextOverflow ellipsisDirection="left">
              {(_b = versionInfo.package) !== null && _b !== void 0 ? _b : '\u2014'}
            </StyledTextOverflow>}/>
        <keyValueTable_1.KeyValueTableRow keyName={locale_1.t('First Event')} value={firstEvent ? <timeSince_1.default date={firstEvent}/> : '\u2014'}/>
        <keyValueTable_1.KeyValueTableRow keyName={locale_1.t('Last Event')} value={lastEvent ? <timeSince_1.default date={lastEvent}/> : '\u2014'}/>
        <keyValueTable_1.KeyValueTableRow keyName={locale_1.t('Source Maps')} value={<link_1.default to={"/settings/" + orgSlug + "/projects/" + projectSlug + "/source-maps/" + encodeURIComponent(version) + "/"}>
              <count_1.default value={releaseMeta.releaseFileCount}/>{' '}
              {locale_1.tn('artifact', 'artifacts', releaseMeta.releaseFileCount)}
            </link_1.default>}/>
      </keyValueTable_1.KeyValueTable>
    </styles_1.Wrapper>);
};
var StyledTextOverflow = styled_1.default(textOverflow_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  line-height: inherit;\n  text-align: right;\n"], ["\n  line-height: inherit;\n  text-align: right;\n"])));
exports.default = ProjectReleaseDetails;
var templateObject_1;
//# sourceMappingURL=projectReleaseDetails.jsx.map