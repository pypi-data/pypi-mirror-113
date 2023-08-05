Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var queryCount_1 = tslib_1.__importDefault(require("app/components/queryCount"));
var locale_1 = require("app/locale");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var mergedItem_1 = tslib_1.__importDefault(require("./mergedItem"));
var mergedToolbar_1 = tslib_1.__importDefault(require("./mergedToolbar"));
function MergedList(_a) {
    var _b = _a.fingerprints, fingerprints = _b === void 0 ? [] : _b, pageLinks = _a.pageLinks, onToggleCollapse = _a.onToggleCollapse, onUnmerge = _a.onUnmerge, organization = _a.organization, groupId = _a.groupId, project = _a.project;
    var fingerprintsWithLatestEvent = fingerprints.filter(function (_a) {
        var latestEvent = _a.latestEvent;
        return !!latestEvent;
    });
    var hasResults = fingerprintsWithLatestEvent.length > 0;
    if (!hasResults) {
        return (<panels_1.Panel>
        <emptyStateWarning_1.default>
          <p>{locale_1.t("There don't seem to be any hashes for this issue.")}</p>
        </emptyStateWarning_1.default>
      </panels_1.Panel>);
    }
    return (<react_1.Fragment>
      <h2>
        <span>{locale_1.t('Merged fingerprints with latest event')}</span>{' '}
        <queryCount_1.default count={fingerprintsWithLatestEvent.length}/>
      </h2>

      <panels_1.Panel>
        <mergedToolbar_1.default onToggleCollapse={onToggleCollapse} onUnmerge={onUnmerge} orgId={organization.slug} project={project} groupId={groupId}/>

        <panels_1.PanelBody>
          {fingerprintsWithLatestEvent.map(function (fingerprint) { return (<mergedItem_1.default key={fingerprint.id} organization={organization} fingerprint={fingerprint}/>); })}
        </panels_1.PanelBody>
      </panels_1.Panel>
      {pageLinks && <pagination_1.default pageLinks={pageLinks}/>}
    </react_1.Fragment>);
}
exports.default = withOrganization_1.default(MergedList);
//# sourceMappingURL=mergedList.jsx.map