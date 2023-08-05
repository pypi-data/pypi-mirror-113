Object.defineProperty(exports, "__esModule", { value: true });
exports.renderMain = void 0;
var tslib_1 = require("tslib");
var constants_1 = require("app/constants");
var main_1 = tslib_1.__importDefault(require("app/main"));
var renderDom_1 = require("./renderDom");
function renderMain() {
    try {
        renderDom_1.renderDom(main_1.default, "#" + constants_1.ROOT_ELEMENT);
    }
    catch (err) {
        if (err.message === 'URI malformed') {
            // eslint-disable-next-line no-console
            console.error(new Error('An unencoded "%" has appeared, it is super effective! (See https://github.com/ReactTraining/history/issues/505)'));
            window.location.assign(window.location.pathname);
        }
    }
}
exports.renderMain = renderMain;
//# sourceMappingURL=renderMain.jsx.map