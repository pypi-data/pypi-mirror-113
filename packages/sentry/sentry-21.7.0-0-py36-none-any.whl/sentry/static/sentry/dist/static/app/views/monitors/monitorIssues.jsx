Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var issueList_1 = tslib_1.__importDefault(require("app/components/issueList"));
var locale_1 = require("app/locale");
var MonitorIssues = function (_a) {
    var orgId = _a.orgId, monitor = _a.monitor;
    return (<issueList_1.default endpoint={"/organizations/" + orgId + "/issues/"} query={{
            query: 'monitor.id:"' + monitor.id + '"',
            project: monitor.project.id,
            limit: 5,
        }} pagination={false} emptyText={locale_1.t('No issues found')} noBorder noMargin/>);
};
exports.default = MonitorIssues;
//# sourceMappingURL=monitorIssues.jsx.map