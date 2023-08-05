Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var marked_1 = tslib_1.__importDefault(require("app/utils/marked"));
var NoteBody = function (_a) {
    var className = _a.className, text = _a.text;
    return (<div className={className} data-test-id="activity-note-body" dangerouslySetInnerHTML={{ __html: marked_1.default(text) }}/>);
};
exports.default = NoteBody;
//# sourceMappingURL=body.jsx.map