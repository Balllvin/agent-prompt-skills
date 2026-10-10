from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from importlib.util import module_from_spec, spec_from_file_location

spec = spec_from_file_location("slice_checker", Path(__file__).with_name("check-slices.py"))
checker = module_from_spec(spec)
spec.loader.exec_module(checker)


def contract(slice_id, tier, owns, depends="none"):
    return f"""## {slice_id} {tier}. Projection
Owns: `{owns}`.
Forbidden: everything else.
Depends: {depends}
Done when: the counted public read stays at one query.
"""


class SliceContractTests(unittest.TestCase):
    def inspect(self, *parts):
        with TemporaryDirectory() as directory:
            paths = []
            for index, text in enumerate(parts):
                path = Path(directory) / f"part-{index}.md"
                path.write_text(text)
                paths.append(path)
            return checker.check(paths)

    def test_collision_in_reserved_path_across_parts_is_rejected(self):
        count, errors = self.inspect(contract("L1A", "easy", "new/projection.py"), contract("L1B", "hard", "new/projection.py"))
        self.assertEqual(count, 2)
        self.assertIn("L1B overlaps L1A: new/projection.py", errors)

    def test_same_file_in_later_layer_is_allowed(self):
        count, errors = self.inspect(contract("L1A", "easy", "app/rows.py"), contract("L2A", "hard", "app/rows.py", "all L1 merged"))
        self.assertEqual((count, errors), (2, []))

    def test_mixed_tiers_and_same_layer_dependency_are_rejected(self):
        _, errors = self.inspect(contract("L1A", "hard-ui", "ui/page.tsx"), contract("L1B", "easy", "app/rows.py", "L1A"))
        self.assertIn("L1: tiers must form easy, easy-ui, hard, hard-ui blocks", errors)
        self.assertIn("L1B: same-layer dependency", errors)

    def test_z_then_aa_uses_letter_sequence(self):
        count, errors = self.inspect(contract("L1Z", "hard", "app/z.py"), contract("L1AA", "hard-ui", "ui/aa.tsx"))
        self.assertEqual((count, errors), (2, []))

    def test_empty_field_cannot_borrow_next_line(self):
        _, errors = self.inspect(contract("L1A", "easy", "app/rows.py").replace("Depends: none", "Depends:"))
        self.assertIn("L1A: missing Depends", errors)

    def test_malformed_heading_is_not_silently_skipped(self):
        _, errors = self.inspect(contract("L1A", "easy", "app/a.py") + contract("L1B", "tiny", "app/b.py"))
        self.assertTrue(any("malformed slice heading" in error for error in errors))

    def test_noncanonical_and_ancestor_paths_are_rejected(self):
        _, errors = self.inspect(contract("L1A", "easy", "app"), contract("L1B", "hard", "app/rows.py"), contract("L1C", "hard", "app/../rows.py"))
        self.assertTrue(any("ancestor ownership overlap" in error for error in errors))
        self.assertIn("L1C: noncanonical owner path app/../rows.py", errors)

    def test_nested_generator_manifest_is_parent_controlled(self):
        _, errors = self.inspect(contract("L1A", "easy", "backend/scripts/shared_frontend_manifest.json"))
        self.assertIn("L1A: parent-controlled path backend/scripts/shared_frontend_manifest.json", errors)

    def test_source_text_deletion_or_syntax_acceptance_is_rejected(self):
        for proof in ("static dead-owner absence check", "source-text deleted-name absence", "source-text syntax assertion"):
            with self.subTest(proof=proof):
                body = contract("L1A", "easy", "app/rows.py").replace("the counted public read stays at one query", proof)
                _, errors = self.inspect(body)
                self.assertIn("L1A: source-text deletion/syntax is not behavior proof; follow AGENTS test policy", errors)

    def test_shipped_strings_and_compiled_contracts_remain_allowed(self):
        for proof in ("the shipped Dockerfile string matches", "the compiled public contract and counted read pass"):
            with self.subTest(proof=proof):
                body = contract("L1A", "easy", "app/rows.py").replace("the counted public read stays at one query", proof)
                self.assertEqual(self.inspect(body), (1, []))

    def test_no_contract_and_shared_control_do_not_pass(self):
        self.assertEqual(self.inspect("# No contracts\n")[1], ["no slice contracts found"])
        _, errors = self.inspect(contract("L1A", "easy", "scripts/ci/local.sh"))
        self.assertIn("L1A: parent-controlled path scripts/ci/local.sh", errors)


if __name__ == "__main__":
    unittest.main()
