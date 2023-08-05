Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var uniq_1 = tslib_1.__importDefault(require("lodash/uniq"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var locale_1 = require("app/locale");
var ownerInput_1 = tslib_1.__importDefault(require("app/views/settings/project/projectOwnership/ownerInput"));
var ProjectOwnershipModal = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectOwnershipModal, _super);
    function ProjectOwnershipModal() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectOwnershipModal.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, issueId = _a.issueId;
        return [
            ['ownership', "/projects/" + organization.slug + "/" + project.slug + "/ownership/"],
            [
                'urlTagData',
                "/issues/" + issueId + "/tags/url/",
                {},
                {
                    allowError: function (error) {
                        // Allow for 404s
                        return error.status === 404;
                    },
                },
            ],
            ['eventData', "/issues/" + issueId + "/events/latest/"],
        ];
    };
    ProjectOwnershipModal.prototype.renderBody = function () {
        var _a, _b, _c, _d, _e, _f, _g;
        var _h = this.state, ownership = _h.ownership, urlTagData = _h.urlTagData, eventData = _h.eventData;
        if (!ownership && !urlTagData && !eventData) {
            return null;
        }
        var urls = urlTagData
            ? urlTagData.topValues
                .sort(function (a, b) { return a.count - b.count; })
                .map(function (i) { return i.value; })
                .slice(0, 5)
            : [];
        // pull frame data out of exception or the stacktrace
        var entry = (eventData === null || eventData === void 0 ? void 0 : eventData.entries).find(function (_a) {
            var type = _a.type;
            return ['exception', 'stacktrace'].includes(type);
        });
        var frames = [];
        if ((entry === null || entry === void 0 ? void 0 : entry.type) === 'exception') {
            frames = (_e = (_d = (_c = (_b = (_a = entry === null || entry === void 0 ? void 0 : entry.data) === null || _a === void 0 ? void 0 : _a.values) === null || _b === void 0 ? void 0 : _b[0]) === null || _c === void 0 ? void 0 : _c.stacktrace) === null || _d === void 0 ? void 0 : _d.frames) !== null && _e !== void 0 ? _e : [];
        }
        if ((entry === null || entry === void 0 ? void 0 : entry.type) === 'stacktrace') {
            frames = (_g = (_f = entry === null || entry === void 0 ? void 0 : entry.data) === null || _f === void 0 ? void 0 : _f.frames) !== null && _g !== void 0 ? _g : [];
        }
        // filter frames by inApp unless there would be 0
        var inAppFrames = frames.filter(function (frame) { return frame.inApp; });
        if (inAppFrames.length > 0) {
            frames = inAppFrames;
        }
        var paths = uniq_1.default(frames.map(function (frame) { return frame.filename || frame.absPath || ''; }))
            .filter(function (i) { return i; })
            .slice(0, 30);
        return (<react_1.Fragment>
        <p>{locale_1.t('Match against Issue Data: (globbing syntax *, ? supported)')}</p>
        <ownerInput_1.default {...this.props} initialText={(ownership === null || ownership === void 0 ? void 0 : ownership.raw) || ''} urls={urls} paths={paths}/>
      </react_1.Fragment>);
    };
    return ProjectOwnershipModal;
}(asyncComponent_1.default));
exports.default = ProjectOwnershipModal;
//# sourceMappingURL=modal.jsx.map